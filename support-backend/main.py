"""GoIPPro AI Support Chat + Voice + Escalation Backend
Port 8085 — chat widget, browser voice, human escalation
"""
import asyncio, json, logging, os, glob, time, uuid, aiohttp
from datetime import datetime, timezone
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, Response
from urllib.parse import quote
import uvicorn
from anthropic import AsyncAnthropic

KB_DIR = "/home/administrator/shared/goippro/knowledge_base"
LOG_DIR = "/var/log/goippro-support"
PORT = 8085
LLM_MODEL = "claude-haiku-4-5-20251001"
MAX_HISTORY = 10

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
DASHBOARD_URL = "https://dashboard.smartcare.house/api/chat/event"
ESCALATION_LOG = os.path.join(LOG_DIR, "escalations.jsonl")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(f"{LOG_DIR}/chat.log", encoding="utf-8")])
logger = logging.getLogger("goippro-support")

# ── Knowledge Base ─────────────────────────────────────
def load_knowledge_base() -> str:
    parts = []
    for fpath in sorted(glob.glob(os.path.join(KB_DIR, "*.md"))):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                parts.append(f.read().strip())
        except Exception as e:
            logger.error(f"KB load error {fpath}: {e}")
    combined = "\n\n---\n\n".join(parts)
    logger.info(f"Loaded {len(parts)} KB files, {len(combined)} chars")
    return combined

KNOWLEDGE_BASE = load_knowledge_base()

# ── System Prompts ─────────────────────────────────────
SYSTEM_PROMPT = f"""You are GoIPPro Support Assistant — an AI support agent for GoIPPro, a B2B platform for GoIP channel rental.

CORE RULES:
1. Answer using ONLY the knowledge base below. Do NOT invent information.
2. If you don't know — say so honestly and offer to connect with a live operator.
3. Be professional, friendly, concise. Light humor OK.
4. ALWAYS respond in the SAME LANGUAGE the user writes in.
5. For earnings — give realistic ranges, not promises.
6. Never share internal technical details (servers, IPs, infrastructure).
7. Keep answers under 200 words unless detailed explanation needed.
8. Use markdown sparingly — bold for emphasis, bullets only for lists.

ESCALATION RULES (critical):
- If you CANNOT answer after 2 attempts → offer live operator.
- If user explicitly asks for a human/operator/person → immediately offer escalation.
- For billing, payment disputes, account issues → always offer live operator.
- For complex technical problems you can't resolve → offer live operator.
- When offering escalation, say something like: "I'd recommend speaking with our team directly. Would you like me to connect you with a live operator?"
- NEVER just dump contact links. Always ASK if they want to be connected first.
- If user confirms they want an operator, respond with EXACTLY this marker: [ESCALATE]
  followed by a friendly message that help is on the way.

CONTEXT:
- GoIPPro is ORIGINATION ONLY (inbound traffic). NOT termination.
- B2B wholesale telecom, not consumer retail.
- Crypto payments (USDT/USDC) — feature, not limitation.

KNOWLEDGE BASE:
{KNOWLEDGE_BASE}

Respond in the user's language. Be helpful. Be honest."""

VOICE_PROMPT_TEMPLATE = """You are GoIPPro Voice Support — a phone agent for GoIPPro, a B2B platform for GoIP channel rental.

RULES:
- VOICE conversation. Max 3 sentences. No markdown/lists. Speak naturally.
- The user speaks {lang_name}. ALWAYS respond in {lang_name}.
- If complex — 2 sentences core + ask if they want details.
- If you CAN'T help — offer to connect with a live person. Say: "Would you like me to connect you with our support team?"

KNOWLEDGE:
GoIPPro: partners connect GoIP devices, earn USDT/USDC. Inbound-only traffic. SIM cards stay safe.
Earnings: GoIP 8 = $80-200/month. GoIP 32 = $250-800+/month. Depends on country/demand.
Start: register goippro.com or Telegram @goippro_support. 10-day validation. Then earn.
Devices: GoIP 4/8/16/32. 1 Mbps per 8 ports. Wired preferred.
Payments: Monthly USDT/USDC (TRC-20/ERC-20). Min $10. Automatic.
Countries: 25+ active — Turkey, Nigeria, Pakistan, India, Brazil, Germany, UK, more.

IF DON'T KNOW: Offer to connect with live operator.
TONE: Professional, friendly, concise. Not pushy. Ranges, not promises."""

LANG_NAMES = {
    "en":"English","ru":"Russian","pt":"Portuguese","es":"Spanish",
    "ar":"Arabic","tr":"Turkish","fr":"French","zh":"Chinese",
    "ko":"Korean","fa":"Persian","ur":"Urdu","de":"German",
    "it":"Italian","hi":"Hindi","ja":"Japanese",
}

# ── Clients ────────────────────────────────────────────
client = AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

VOICE_ENABLED = False
voice = None
try:
    from voice_handler import VoiceHandler
    voice = VoiceHandler()
    VOICE_ENABLED = True
    logger.info("Voice support ENABLED")
except Exception as e:
    logger.warning(f"Voice disabled: {e}")

# ── Sessions ───────────────────────────────────────────
sessions: dict[str, list] = {}
SESSION_TTL = 3600

def get_session(sid: str) -> list:
    if sid not in sessions: sessions[sid] = []
    return sessions[sid]

def cleanup_sessions():
    now = time.time()
    for sid in [s for s, m in sessions.items() if m and (now - m[-1].get("_ts", 0)) > SESSION_TTL]:
        del sessions[sid]

def detect_language(text: str) -> str:
    for ch in text:
        if '\u0400' <= ch <= '\u04FF': return "ru"
        if '\u0600' <= ch <= '\u06FF': return "ar"
        if '\u4E00' <= ch <= '\u9FFF': return "zh"
        if '\uAC00' <= ch <= '\uD7AF': return "ko"
    if any(c in set("İıŞşĞğÜüÖöÇç") for c in text): return "tr"
    if any(c in set("ãõ") for c in text): return "pt"
    return "en"

def log_question(sid, question, answer, language):
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "session_id": sid,
             "question": question, "answer_preview": answer[:200], "language": language}
    try:
        with open(os.path.join(LOG_DIR, f"questions_{datetime.now().strftime('%Y-%m')}.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        logger.error(f"Log error: {e}")

# ── Escalation ─────────────────────────────────────────
async def notify_escalation(session_id: str, lang: str, history: list, reason: str, contact: str = ""):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    for m in history[-8:]:
        r = "👤" if m["role"] == "user" else "🤖"
        t = m["content"][:200].replace("[VOICE] ", "🎤 ")
        lines.append(f"{r} {t}")
    summary = "\n".join(lines)

    # Log
    entry = {"timestamp": ts, "session_id": session_id, "language": lang,
             "reason": reason, "contact": contact, "conversation": summary}
    try:
        with open(ESCALATION_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except: pass

    # Dashboard
    try:
        async with aiohttp.ClientSession() as s:
            await s.post(DASHBOARD_URL, json={
                "chat_id": "goippro_devops",
                "action": f"🚨 Support escalation [{lang.upper()}]",
                "details": f"Reason: {reason}\nContact: {contact or 'N/A'}\n\n{summary[:500]}"
            }, timeout=aiohttp.ClientTimeout(total=5))
    except Exception as e:
        logger.error(f"Dashboard notify error: {e}")

    # Telegram (may fail if bot blocked)
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        tg = (f"🚨 <b>GoIPPro Escalation</b>\n⏰ {ts}\n🌐 {lang.upper()}\n"
              f"📝 {reason}\n👤 Contact: {contact or 'N/A'}\n\n<pre>{summary[:600]}</pre>")
        try:
            async with aiohttp.ClientSession() as s:
                await s.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                    data={"chat_id": TELEGRAM_CHAT_ID, "text": tg, "parse_mode": "HTML"},
                    timeout=aiohttp.ClientTimeout(total=5))
        except: pass

    logger.info(f"Escalation: session={session_id}, lang={lang}, reason={reason}")

ESCALATION_RESPONSES = {
    "en": "I've notified our support team — they'll reach out to you shortly! In the meantime, you can also contact us directly:\n\n📱 **Telegram**: [@goippro_support](https://t.me/goippro_support)\n📧 **Email**: support@goippro.com",
    "ru": "Я уведомил нашу команду поддержки — они скоро свяжутся с вами! Также можете связаться напрямую:\n\n📱 **Telegram**: [@goippro_support](https://t.me/goippro_support)\n📧 **Email**: support@goippro.com",
    "tr": "Destek ekibimize bildirdim — en kısa sürede size ulaşacaklar! Doğrudan da iletişime geçebilirsiniz:\n\n📱 **Telegram**: [@goippro_support](https://t.me/goippro_support)\n📧 **Email**: support@goippro.com",
    "ar": "لقد أبلغت فريق الدعم — سيتواصلون معك قريبًا! يمكنك أيضًا التواصل مباشرة:\n\n📱 **Telegram**: [@goippro_support](https://t.me/goippro_support)\n📧 **Email**: support@goippro.com",
    "pt": "Notifiquei nossa equipe — entrarão em contato em breve! Você também pode nos contatar:\n\n📱 **Telegram**: [@goippro_support](https://t.me/goippro_support)\n📧 **Email**: support@goippro.com",
    "es": "He notificado a nuestro equipo — se pondrán en contacto pronto! También puedes contactarnos:\n\n📱 **Telegram**: [@goippro_support](https://t.me/goippro_support)\n📧 **Email**: support@goippro.com",
}

# ── FastAPI App ────────────────────────────────────────
app = FastAPI(title="GoIPPro Support", version="3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
    expose_headers=["X-Transcript-User","X-Transcript-Bot","X-Language","X-Session-Id"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": "goippro-support", "version": "3.0",
            "kb_files": len(glob.glob(os.path.join(KB_DIR, "*.md"))), "voice": VOICE_ENABLED}

@app.get("/api/stats")
async def stats():
    esc_count = 0
    try:
        with open(ESCALATION_LOG) as f: esc_count = sum(1 for _ in f)
    except: pass
    return {"active_sessions": len(sessions), "kb_files": len(glob.glob(os.path.join(KB_DIR, "*.md"))),
            "kb_size_chars": len(KNOWLEDGE_BASE), "voice_enabled": VOICE_ENABLED, "escalations": esc_count}

# ── Chat ───────────────────────────────────────────────
@app.post("/api/chat")
async def chat(request: Request):
    try: body = await request.json()
    except: return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    message = body.get("message", "").strip()
    if not message: return JSONResponse({"error": "Empty message"}, status_code=400)
    if len(message) > 2000: return JSONResponse({"error": "Message too long"}, status_code=400)

    session_id = body.get("session_id") or str(uuid.uuid4())
    history = get_session(session_id)
    messages = [{"role": h["role"], "content": h["content"]} for h in history[-MAX_HISTORY:]]
    messages.append({"role": "user", "content": message})

    try:
        response = await client.messages.create(model=LLM_MODEL, system=SYSTEM_PROMPT, messages=messages, max_tokens=800)
        answer = response.content[0].text
        history.append({"role": "user", "content": message, "_ts": time.time()})
        history.append({"role": "assistant", "content": answer, "_ts": time.time()})
        lang = detect_language(message)
        log_question(session_id, message, answer, lang)
        if len(sessions) > 100: cleanup_sessions()

        # Check if AI triggered escalation
        auto_escalate = "[ESCALATE]" in answer
        if auto_escalate:
            answer = answer.replace("[ESCALATE]", "").strip()
            await notify_escalation(session_id, lang, history, "AI-triggered escalation")

        return JSONResponse({"answer": answer, "session_id": session_id, "escalated": auto_escalate})
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return JSONResponse({"answer": "Sorry, I'm having trouble. Please contact @goippro_support",
                             "session_id": session_id, "error": True}, status_code=500)

@app.post("/api/chat/stream")
async def chat_stream(request: Request):
    try: body = await request.json()
    except: return JSONResponse({"error": "Invalid JSON"}, status_code=400)
    message = body.get("message", "").strip()
    if not message: return JSONResponse({"error": "Empty message"}, status_code=400)
    session_id = body.get("session_id") or str(uuid.uuid4())
    history = get_session(session_id)
    messages = [{"role": h["role"], "content": h["content"]} for h in history[-MAX_HISTORY:]]
    messages.append({"role": "user", "content": message})

    async def generate():
        full = ""
        try:
            async with client.messages.stream(model=LLM_MODEL, system=SYSTEM_PROMPT, messages=messages, max_tokens=800) as stream:
                async for text in stream.text_stream:
                    full += text
                    yield f"data: {json.dumps({'token': text})}\n\n"
            history.append({"role": "user", "content": message, "_ts": time.time()})
            history.append({"role": "assistant", "content": full, "_ts": time.time()})
            log_question(session_id, message, full, detect_language(message))
            escalated = "[ESCALATE]" in full
            if escalated:
                await notify_escalation(session_id, detect_language(message), history, "AI-triggered escalation")
            yield f"data: {json.dumps({'done': True, 'session_id': session_id, 'escalated': escalated})}\n\n"
        except Exception as e:
            logger.error(f"Stream error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")

# ── Voice ──────────────────────────────────────────────
@app.post("/api/voice")
async def voice_chat(audio: UploadFile = File(...), session_id: str = Form(default="")):
    if not VOICE_ENABLED: return JSONResponse({"error": "Voice not available"}, status_code=503)
    try:
        audio_bytes = await audio.read()
        if len(audio_bytes) < 1000: return JSONResponse({"error": "Audio too short"}, status_code=400)
        if len(audio_bytes) > 10_000_000: return JSONResponse({"error": "Audio too large"}, status_code=400)

        stt_result = voice.speech_to_text(audio_bytes, filename=audio.filename or "audio.webm")
        user_text, detected_lang = stt_result["text"], stt_result["language"]
        if not user_text or len(user_text.strip()) < 2:
            return JSONResponse({"error": "Could not understand audio"}, status_code=400)

        if not session_id: session_id = str(uuid.uuid4())
        history = get_session(session_id)
        messages = [{"role": h["role"], "content": h["content"]} for h in history[-MAX_HISTORY:]]
        messages.append({"role": "user", "content": user_text})

        lang_name = LANG_NAMES.get(detected_lang, "English")
        voice_prompt = VOICE_PROMPT_TEMPLATE.format(lang_name=lang_name)
        response = await client.messages.create(model=LLM_MODEL, system=voice_prompt, messages=messages, max_tokens=300)
        answer_text = response.content[0].text

        history.append({"role": "user", "content": user_text, "_ts": time.time()})
        history.append({"role": "assistant", "content": answer_text, "_ts": time.time()})
        log_question(session_id, f"[VOICE] {user_text}", answer_text, detected_lang)

        audio_response = voice.text_to_speech(answer_text, language=detected_lang)
        return Response(content=audio_response, media_type="audio/mpeg", headers={
            "X-Transcript-User": quote(user_text, safe=""),
            "X-Transcript-Bot": quote(answer_text, safe=""),
            "X-Language": detected_lang.lower()[:2], "X-Session-Id": session_id})
    except Exception as e:
        logger.error(f"Voice error: {e}", exc_info=True)
        return JSONResponse({"error": f"Voice failed: {str(e)}"}, status_code=500)

@app.get("/api/voice/status")
async def voice_status():
    return {"voice_enabled": VOICE_ENABLED}

# ── Escalation ─────────────────────────────────────────
@app.post("/api/escalate")
async def escalate(request: Request):
    """Manual escalation — user clicked 'Talk to human'."""
    try: body = await request.json()
    except: return JSONResponse({"error": "Invalid JSON"}, status_code=400)

    session_id = body.get("session_id", "")
    reason = body.get("reason", "User requested human support")
    contact = body.get("contact", "")
    history = get_session(session_id) if session_id else []

    lang = body.get("language", "en")
    if lang == "en":
        for msg in reversed(history):
            if msg["role"] == "user":
                lang = detect_language(msg["content"])
                break

    await notify_escalation(session_id, lang, history, reason, contact)
    msg = ESCALATION_RESPONSES.get(lang, ESCALATION_RESPONSES["en"])

    if session_id:
        get_session(session_id).append({"role": "assistant", "content": msg, "_ts": time.time()})

    return JSONResponse({"escalated": True, "message": msg, "session_id": session_id,
        "contacts": {"telegram": "https://t.me/goippro_support", "email": "support@goippro.com"}})

# ── KB Reload ──────────────────────────────────────────
@app.post("/api/kb/reload")
async def reload_kb():
    global KNOWLEDGE_BASE, SYSTEM_PROMPT
    KNOWLEDGE_BASE = load_knowledge_base()
    SYSTEM_PROMPT = SYSTEM_PROMPT.split("KNOWLEDGE BASE:")[0] + f"KNOWLEDGE BASE:\n{KNOWLEDGE_BASE}\n\nRespond in the user's language. Be helpful. Be honest."
    return {"status": "reloaded", "kb_size": len(KNOWLEDGE_BASE)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
