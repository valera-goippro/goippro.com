"""GoIPPro AI Support Chat + Voice Backend
Port 8085 — serves chat widget and voice on goippro.com
Uses Anthropic Claude with knowledge base context
Groq Whisper STT + OpenAI TTS for voice
"""
import asyncio
import json
import logging
import os
import glob
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, Response
import uvicorn
from anthropic import AsyncAnthropic

# ── Config ─────────────────────────────────────────────
KB_DIR = "/home/administrator/shared/goippro/knowledge_base"
LOG_DIR = "/var/log/goippro-support"
PORT = 8085
LLM_MODEL = "claude-haiku-4-5-20251001"
MAX_HISTORY = 10

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"{LOG_DIR}/chat.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger("goippro-support")

# ── Knowledge Base ─────────────────────────────────────
def load_knowledge_base() -> str:
    kb_parts = []
    files = sorted(glob.glob(os.path.join(KB_DIR, "*.md")))
    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read().strip()
                kb_parts.append(content)
        except Exception as e:
            logger.error(f"Error loading {fpath}: {e}")
    combined = "\n\n---\n\n".join(kb_parts)
    logger.info(f"Loaded {len(files)} KB files, {len(combined)} chars")
    return combined

KNOWLEDGE_BASE = load_knowledge_base()

# ── System Prompt (Chat) ──────────────────────────────
SYSTEM_PROMPT = f"""You are GoIPPro Support Assistant — an AI support agent for GoIPPro, a B2B platform for GoIP channel rental.

CORE RULES:
1. Answer questions using ONLY the knowledge base below. Do NOT invent information.
2. If you don't know the answer, say so honestly and suggest contacting human support: Telegram @goippro_support or email support@goippro.com
3. Be professional, friendly, and concise. Light humor is OK when appropriate.
4. ALWAYS respond in the SAME LANGUAGE the user writes in. If they write in Russian, respond in Russian. Turkish → Turkish. Arabic → Arabic. Etc.
5. For earnings questions, give realistic ranges, not promises. Use the calculator data.
6. Never share internal technical details about servers, IPs, or infrastructure.
7. You represent GoIPPro as a company. Be helpful, not salesy.
8. For complex technical issues, recommend contacting support directly.
9. Keep answers focused and under 200 words unless a detailed explanation is needed.
10. Use markdown formatting sparingly — bold for emphasis, bullet points only when listing multiple items.

IMPORTANT CONTEXT:
- GoIPPro is ORIGINATION ONLY (inbound traffic). We are NOT a termination platform.
- This is a B2B service for wholesale telecom traffic, not consumer retail.
- Payments are in crypto (USDT/USDC) — this is a feature, not a limitation.

KNOWLEDGE BASE:
{KNOWLEDGE_BASE}

Remember: respond in the user's language. Be helpful. Be honest."""

# ── System Prompt (Voice — shorter, conversational) ───
VOICE_SYSTEM_PROMPT_TEMPLATE = """You are GoIPPro Voice Support — a phone agent for GoIPPro, a B2B platform for GoIP channel rental.

CRITICAL RULES:
- This is a VOICE conversation. Keep answers SHORT — max 3 sentences.
- No markdown, no lists, no bullet points, no headers. Speak naturally like a human on the phone.
- The user is speaking {lang_name}. ALWAYS respond in {lang_name}.
- If the topic is complex, give the core idea in 2 sentences and ask if they want details.

WHAT YOU KNOW:
GoIPPro: B2B platform, partners connect GoIP devices, earn passive income in USDT/USDC crypto.
Inbound-only traffic — devices receive calls, never make outgoing. SIM cards stay safe.
Earnings: GoIP 8 = $80-200/month, GoIP 32 = $250-800+/month. Depends on country and demand.
How to start: Register on goippro.com or Telegram @goippro_support, submit device info, 10-day validation, then earn.
Supported devices: GoIP 4, 8, 16, 32. Need stable internet, 1 Mbps per 8 ports.
Payments: Monthly USDT/USDC on TRC-20 or ERC-20. Minimum $10. Automatic.
Countries: 25+ active markets including Turkey, Nigeria, Pakistan, India, Brazil, Germany, UK, and more.

IF YOU DON'T KNOW: Say you'll connect them with the team — Telegram @goippro_support or email support@goippro.com.

TONE: Professional, friendly, concise. Never pushy. Give ranges, not promises."""

LANG_NAMES = {
    "en": "English", "ru": "Russian", "pt": "Portuguese", "es": "Spanish",
    "ar": "Arabic", "tr": "Turkish", "fr": "French", "zh": "Chinese",
    "ko": "Korean", "fa": "Persian", "ur": "Urdu", "de": "German",
    "it": "Italian", "hi": "Hindi", "ja": "Japanese", "nl": "Dutch",
    "pl": "Polish", "vi": "Vietnamese", "th": "Thai", "id": "Indonesian",
}

# ── Clients ────────────────────────────────────────────
client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Voice handler (optional — degrades gracefully)
VOICE_ENABLED = False
voice = None
try:
    from voice_handler import VoiceHandler
    voice = VoiceHandler()
    VOICE_ENABLED = True
    logger.info("Voice support ENABLED")
except Exception as e:
    logger.warning(f"Voice support disabled: {e}")

# ── Session Storage ────────────────────────────────────
sessions: dict[str, list] = {}
SESSION_TTL = 3600

def get_session(session_id: str) -> list:
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]

def cleanup_sessions():
    now = time.time()
    to_remove = [sid for sid, msgs in sessions.items()
                 if msgs and (now - msgs[-1].get("_ts", 0)) > SESSION_TTL]
    for sid in to_remove:
        del sessions[sid]

# ── Question Logger ────────────────────────────────────
def log_question(session_id: str, question: str, answer: str, language: str):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "question": question,
        "answer_preview": answer[:200],
        "language": language,
    }
    log_file = os.path.join(LOG_DIR, f"questions_{datetime.now().strftime('%Y-%m')}.jsonl")
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.error(f"Error logging question: {e}")

# ── Language Detection (text) ──────────────────────────
def detect_language(text: str) -> str:
    for ch in text:
        if '\u0400' <= ch <= '\u04FF': return "ru"
        if '\u0600' <= ch <= '\u06FF': return "ar"
        if '\u4E00' <= ch <= '\u9FFF': return "zh"
        if '\uAC00' <= ch <= '\uD7AF': return "ko"
    turkish = set("İıŞşĞğÜüÖöÇç")
    if any(c in turkish for c in text): return "tr"
    portuguese = set("ãõçÇ")
    if any(c in portuguese for c in text): return "pt"
    return "en"

# ── FastAPI App ────────────────────────────────────────
app = FastAPI(title="GoIPPro Support Chat + Voice", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Transcript-User", "X-Transcript-Bot", "X-Language", "X-Session-Id"],
)

# ── Health & Stats ─────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "service": "goippro-support", "kb_files": len(glob.glob(os.path.join(KB_DIR, "*.md"))), "voice": VOICE_ENABLED}

@app.get("/api/stats")
async def stats():
    return {"active_sessions": len(sessions), "kb_files": len(glob.glob(os.path.join(KB_DIR, "*.md"))), "kb_size_chars": len(KNOWLEDGE_BASE), "voice_enabled": VOICE_ENABLED}

# ── Chat Endpoints ─────────────────────────────────────
@app.post("/api/chat")
async def chat(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    message = body.get("message", "").strip()
    if not message:
        return JSONResponse({"error": "Empty message"}, status_code=400)
    if len(message) > 2000:
        return JSONResponse({"error": "Message too long"}, status_code=400)

    session_id = body.get("session_id") or str(uuid.uuid4())
    history = get_session(session_id)

    messages = [{"role": h["role"], "content": h["content"]} for h in history[-MAX_HISTORY:]]
    messages.append({"role": "user", "content": message})

    try:
        response = await client.messages.create(model=LLM_MODEL, system=SYSTEM_PROMPT, messages=messages, max_tokens=800)
        answer = response.content[0].text

        history.append({"role": "user", "content": message, "_ts": time.time()})
        history.append({"role": "assistant", "content": answer, "_ts": time.time()})
        log_question(session_id, message, answer, detect_language(message))
        if len(sessions) > 100: cleanup_sessions()

        return JSONResponse({"answer": answer, "session_id": session_id})
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return JSONResponse({"answer": "Sorry, I'm having trouble right now. Please try again or contact support: @goippro_support", "session_id": session_id, "error": True}, status_code=500)

@app.post("/api/chat/stream")
async def chat_stream(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    message = body.get("message", "").strip()
    if not message:
        return JSONResponse({"error": "Empty message"}, status_code=400)

    session_id = body.get("session_id") or str(uuid.uuid4())
    history = get_session(session_id)

    messages = [{"role": h["role"], "content": h["content"]} for h in history[-MAX_HISTORY:]]
    messages.append({"role": "user", "content": message})

    async def generate():
        full_answer = ""
        try:
            async with client.messages.stream(model=LLM_MODEL, system=SYSTEM_PROMPT, messages=messages, max_tokens=800) as stream:
                async for text in stream.text_stream:
                    full_answer += text
                    yield f"data: {json.dumps({'token': text})}\n\n"
            history.append({"role": "user", "content": message, "_ts": time.time()})
            history.append({"role": "assistant", "content": full_answer, "_ts": time.time()})
            log_question(session_id, message, full_answer, detect_language(message))
            yield f"data: {json.dumps({'done': True, 'session_id': session_id})}\n\n"
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

# ── Voice Endpoint ─────────────────────────────────────
@app.post("/api/voice")
async def voice_chat(audio: UploadFile = File(...), session_id: str = Form(default="")):
    """Accept audio, return audio response. Auto-detects language."""
    if not VOICE_ENABLED:
        return JSONResponse({"error": "Voice support not available"}, status_code=503)

    try:
        audio_bytes = await audio.read()
        if len(audio_bytes) < 1000:
            return JSONResponse({"error": "Audio too short"}, status_code=400)
        if len(audio_bytes) > 10_000_000:
            return JSONResponse({"error": "Audio too large (max 10MB)"}, status_code=400)

        # STT
        stt_result = voice.speech_to_text(audio_bytes, filename=audio.filename or "audio.webm")
        user_text = stt_result["text"]
        detected_lang = stt_result["language"]

        if not user_text or len(user_text.strip()) < 2:
            return JSONResponse({"error": "Could not understand audio", "text": ""}, status_code=400)

        # Session
        if not session_id:
            session_id = str(uuid.uuid4())
        history = get_session(session_id)

        messages = [{"role": h["role"], "content": h["content"]} for h in history[-MAX_HISTORY:]]
        messages.append({"role": "user", "content": user_text})

        # LLM with voice-optimized prompt
        lang_name = LANG_NAMES.get(detected_lang, "English")
        voice_prompt = VOICE_SYSTEM_PROMPT_TEMPLATE.format(lang_name=lang_name)

        response = await client.messages.create(model=LLM_MODEL, system=voice_prompt, messages=messages, max_tokens=300)
        answer_text = response.content[0].text

        history.append({"role": "user", "content": user_text, "_ts": time.time()})
        history.append({"role": "assistant", "content": answer_text, "_ts": time.time()})
        log_question(session_id, f"[VOICE] {user_text}", answer_text, detected_lang)

        # TTS
        audio_response = voice.text_to_speech(answer_text, language=detected_lang)

        # URL-encode transcripts for safe HTTP headers
        from urllib.parse import quote
        return Response(
            content=audio_response,
            media_type="audio/mpeg",
            headers={
                "X-Transcript-User": quote(user_text, safe=""),
                "X-Transcript-Bot": quote(answer_text, safe=""),
                "X-Language": detected_lang.lower()[:2],
                "X-Session-Id": session_id,
            },
        )
    except Exception as e:
        logger.error(f"Voice error: {e}", exc_info=True)
        return JSONResponse({"error": f"Voice processing failed: {str(e)}"}, status_code=500)

@app.get("/api/voice/status")
async def voice_status():
    return {"voice_enabled": VOICE_ENABLED}

# ── KB Reload ──────────────────────────────────────────
@app.post("/api/kb/reload")
async def reload_kb():
    global KNOWLEDGE_BASE, SYSTEM_PROMPT
    KNOWLEDGE_BASE = load_knowledge_base()
    SYSTEM_PROMPT = SYSTEM_PROMPT.split("KNOWLEDGE BASE:")[0] + f"KNOWLEDGE BASE:\n{KNOWLEDGE_BASE}\n\nRemember: respond in the user's language. Be helpful. Be honest."
    return {"status": "reloaded", "kb_size": len(KNOWLEDGE_BASE)}

# ── Entry Point ────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
