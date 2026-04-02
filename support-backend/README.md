# GoIPPro AI Support Backend

## Chat API (Port 8085)
```bash
pip install -r requirements.txt
ANTHROPIC_API_KEY=sk-... python3 main.py
```

## Endpoints
- `POST /api/chat` — send message, get response
- `POST /api/chat/stream` — SSE streaming response
- `POST /api/kb/reload` — reload knowledge base
- `GET /api/stats` — session/KB stats
- `GET /health` — health check

## Knowledge Base
Markdown files in `knowledge_base/`. Edit and call `/api/kb/reload`.

## Question Analysis
```bash
python3 analyze_questions.py
```

## Voice Config
`voice_config.yaml` — for FreeSWITCH AI Gateway.
