# Deployment Guide

Aerulias AI now has a FastAPI backend in `api_server.py`.

## Local FastAPI Run

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the API and dashboard:

```powershell
uvicorn api_server:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Main API Routes

```text
GET  /health
POST /pipeline/run
POST /demo/run
GET  /memory
GET  /history
GET  /
```

## Deploy On Render

1. Push this project to GitHub.
2. Create a new Render Web Service.
3. Connect your GitHub repository.
4. Render can detect `render.yaml`, or you can use these settings manually:

```text
Build Command: pip install -r requirements.txt
Start Command: uvicorn api_server:app --host 0.0.0.0 --port $PORT
```

5. Add environment variables:

```text
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_SITE_URL=https://your-render-url.onrender.com
OPENROUTER_APP_NAME=aerulias_ai
```

6. Open the deployed URL.

The repository includes `render.yaml`, so Render can also deploy it as a Blueprint.

## Deploy On Railway

1. Push to GitHub.
2. Create a Railway project from the repository.
3. Add the same environment variables.
4. Railway can use the `Procfile`, or you can set the start command:

```text
uvicorn api_server:app --host 0.0.0.0 --port $PORT
```

## Safe Public Demo

For public demos, use the dashboard's Demo mode. Demo mode does not spend API credits and does not require the OpenRouter API to succeed.

## Important Security Notes

- Do not commit `.env`.
- Rotate any API key that was pasted into chat or shared publicly.
- Add rate limiting before exposing a live API with real paid credentials.
