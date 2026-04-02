"""GoIPPro AI Support Chat Backend
Port 8085 — serves chat widget on goippro.com
Uses Anthropic Claude with knowledge base context
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

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
from anthropic import AsyncAnthropic

# ── Config ─────────────────────────────────────────────
KB_DIR = "/home/administrator/shared/goippro/knowledge_base"
LOG_DIR = "/var/log/goippro-support"
PORT = 8085
LLM_MODEL = "claude-haiku-4-5-20251001"
MAX_HISTORY = 10  # max conversation turns to keep

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
    """Load all markdown files from knowledge base directory."""
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

# ── System Prompt ──────────────────────────────────────
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

# ── Anthropic Client ───────────────────────────────────
client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ── Session Storage (in-memory, simple) ────────────────
sessions: dict[str, list] = {}
SESSION_TTL = 3600  # 1 hour

def get_session(session_id: str) -> list:
    if session_id not in sessions:
        sessions[session_id] = []
    return sessions[session_id]

def cleanup_sessions():
    """Remove old sessions."""
    now = time.time()
    to_remove = []
    for sid, msgs in sessions.items():
        if msgs and (now - msgs[-1].get("_ts", 0)) > SESSION_TTL:
            to_remove.append(sid)
    for sid in to_remove:
        del sessions[sid]

# ── Question Logger ────────────────────────────────────
def log_question(session_id: str, question: str, answer: str, language: str):
    """Log questions for learning/analysis."""
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

# ── Language Detection (simple) ────────────────────────
def detect_language(text: str) -> str:
    """Simple language detection by character ranges."""
    for ch in text:
        if '\u0400' <= ch <= '\u04FF':
            return "ru"
        if '\u0600' <= ch <= '\u06FF':
            return "ar"
        if '\u4E00' <= ch <= '\u9FFF':
            return "zh"
        if '\uAC00' <= ch <= '\uD7AF':
            return "ko"
    # Check for Turkish/Portuguese specific chars
    turkish = set("İıŞşĞğÜüÖöÇç")
    if any(c in turkish for c in text):
        return "tr"
    portuguese = set("ãõçÇ")
    if any(c in portuguese for c in text):
        return "pt"
    return "en"

# ── FastAPI App ────────────────────────────────────────
app = FastAPI(title="GoIPPro Support Chat", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "goippro-support", "kb_files": len(glob.glob(os.path.join(KB_DIR, "*.md")))}

@app.post("/api/chat")
async def chat(request: Request):
    """Handle chat message. Expects JSON: {message, session_id?}"""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    message = body.get("message", "").strip()
    if not message:
        return JSONResponse({"error": "Empty message"}, status_code=400)
    if len(message) > 2000:
        return JSONResponse({"error": "Message too long (max 2000 chars)"}, status_code=400)

    session_id = body.get("session_id") or str(uuid.uuid4())
    history = get_session(session_id)

    # Build messages
    messages = []
    for h in history[-MAX_HISTORY:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": message})

    try:
        response = await client.messages.create(
            model=LLM_MODEL,
            system=SYSTEM_PROMPT,
            messages=messages,
            max_tokens=800,
        )
        answer = response.content[0].text

        # Save to session
        history.append({"role": "user", "content": message, "_ts": time.time()})
        history.append({"role": "assistant", "content": answer, "_ts": time.time()})

        # Log for learning
        lang = detect_language(message)
        log_question(session_id, message, answer, lang)

        # Periodic cleanup
        if len(sessions) > 100:
            cleanup_sessions()

        return JSONResponse({
            "answer": answer,
            "session_id": session_id,
        })

    except Exception as e:
        logger.error(f"LLM error: {e}")
        return JSONResponse({
            "answer": "Sorry, I'm having trouble right now. Please try again or contact support: @goippro_support",
            "session_id": session_id,
            "error": True,
        }, status_code=500)

@app.post("/api/chat/stream")
async def chat_stream(request: Request):
    """Streaming chat endpoint for real-time response."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    message = body.get("message", "").strip()
    if not message:
        return JSONResponse({"error": "Empty message"}, status_code=400)

    session_id = body.get("session_id") or str(uuid.uuid4())
    history = get_session(session_id)

    messages = []
    for h in history[-MAX_HISTORY:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": message})

    async def generate():
        full_answer = ""
        try:
            async with client.messages.stream(
                model=LLM_MODEL,
                system=SYSTEM_PROMPT,
                messages=messages,
                max_tokens=800,
            ) as stream:
                async for text in stream.text_stream:
                    full_answer += text
                    yield f"data: {json.dumps({'token': text})}\n\n"

            # Save to session after complete
            history.append({"role": "user", "content": message, "_ts": time.time()})
            history.append({"role": "assistant", "content": full_answer, "_ts": time.time()})
            lang = detect_language(message)
            log_question(session_id, message, full_answer, lang)

            yield f"data: {json.dumps({'done': True, 'session_id': session_id})}\n\n"

        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.post("/api/kb/reload")
async def reload_kb():
    """Reload knowledge base from disk."""
    global KNOWLEDGE_BASE, SYSTEM_PROMPT
    KNOWLEDGE_BASE = load_knowledge_base()
    # Rebuild system prompt
    SYSTEM_PROMPT = SYSTEM_PROMPT.split("KNOWLEDGE BASE:")[0] + f"KNOWLEDGE BASE:\n{KNOWLEDGE_BASE}\n\nRemember: respond in the user's language. Be helpful. Be honest."
    return {"status": "reloaded", "kb_size": len(KNOWLEDGE_BASE)}

@app.get("/api/stats")
async def stats():
    """Basic stats."""
    return {
        "active_sessions": len(sessions),
        "kb_files": len(glob.glob(os.path.join(KB_DIR, "*.md"))),
        "kb_size_chars": len(KNOWLEDGE_BASE),
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
