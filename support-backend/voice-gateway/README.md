# GoIPPro Voice Support Gateway

Standalone FreeSWITCH AI voice agent for GoIPPro support calls.
Listens on ESL port 9003. Auto-detects caller language.

## Pipeline
```
Phone Call → FreeSWITCH → ESL (:9003) → Groq Whisper STT → Claude Haiku → OpenAI TTS → Caller
```

## FreeSWITCH Extension
Dial `9003` or route DID to `goippro`/`support` destination.

## Service
```bash
systemctl status goippro-voice-gw
```

## Dependencies
Same as the main AI gateway (openai, anthropic, groq, websockets, webrtcvad, etc.)
