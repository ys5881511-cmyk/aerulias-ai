# Resume And LinkedIn Guide

## Resume Project Title

Aerulias AI: Self-Improving Multi-Agent Answer System

## Resume Bullets

- Built a multi-agent AI pipeline in Python that generates, evaluates, refines, and stores lessons from AI answers using OpenRouter and structured JSON.
- Implemented a configurable quality loop with target scores, memory retrieval, source-grounded answering, benchmarking, model comparison, and a web dashboard.
- Added FastAPI backend, unit tests, GitHub Actions, documentation, and portfolio-ready demo mode for reliable presentations without spending API credits.

## LinkedIn Post Draft

I built Aerulias AI, a self-improving multi-agent answer system.

Instead of trusting the first AI response, the system:

1. Generates an answer.
2. Evaluates it for correctness, clarity, completeness, and hallucination risk.
3. Refines weak parts.
4. Stores useful lessons in memory.
5. Shows the full process in an interactive dashboard.

I also added source-grounded answering, benchmark mode, model comparison, unit tests, and a demo mode that works without API calls. This project helped me practice AI orchestration, prompt engineering, structured outputs, backend design, testing, and user-facing product design.

## Demo Checklist

1. Start the dashboard:

```powershell
python dashboard_server.py
```

2. Open:

```text
http://127.0.0.1:8000
```

3. Turn on Demo mode for a safe presentation.
4. Run the pipeline.
5. Show the score dial, improvement rounds, memory, and portfolio summary.
6. Copy the LinkedIn draft from the dashboard.

## Interview Explanation

Aerulias AI is designed around reliability. A single model response can be wrong, vague, or incomplete. My system wraps the model with an improvement loop: generation, evaluation, refinement, memory, source grounding, and measurement. This makes the output easier to inspect and improve.
