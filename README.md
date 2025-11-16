# AI Customer Support Chatbot (v2)

This repository contains a production-ready AI customer support chatbot with:
- Gemini SDK support (if `google-generativeai` is installed) with HTTP fallback
- Rate limiting via `flask-limiter`
- Simple client-key based frontend authentication
- Unit tests (pytest) and GitHub Actions CI workflow
- Improved frontend UI with spinner and better UX

See `.env.example` for required environment variables.

Quick local test:
1. Copy `.env.example` to `.env` and set values.
2. Create virtualenv and install: `pip install -r requirements.txt`
3. Run tests: `pytest`
4. Start app: `python app.py`
5. Visit `http://127.0.0.1:5000` and ensure FRONTEND_KEY in `templates/index.html` matches `.env` FRONTEND_API_KEY.

