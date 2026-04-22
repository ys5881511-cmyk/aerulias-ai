# Aerulias AI

Aerulias AI is a small multi-agent answer improvement pipeline.

It uses OpenRouter through the OpenAI Python SDK to:

1. Generate an initial answer.
2. Evaluate the answer for correctness, completeness, clarity, and hallucination risk.
3. Refine the answer using the evaluator feedback.
4. Repeat refinement for multiple rounds until a target score is reached.
5. Save useful mistakes and lessons into local memory for future runs.
6. Save run history for demos and analysis.

## Project Structure

```text
aerulias_ai/
  agents/
    generator.py   # Creates the first answer
    evaluator.py   # Scores and critiques the answer
    refiner.py     # Improves the answer using evaluator feedback
    memory.py      # Loads and saves local mistake memory
    pipeline.py    # Runs multi-round generate/evaluate/refine loops
    common.py      # Shared OpenRouter client and JSON helpers
    main.py        # Runs the complete pipeline
  test_pipeline.py # Quick pipeline test script
  dashboard_server.py # Local web dashboard server
  web/             # Dashboard HTML, CSS, and JavaScript
  .env.example     # Example environment variables
  ROADMAP.md       # Feature roadmap for a stronger portfolio project
  docs/            # Architecture and demo materials
```

## Setup

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-4o-mini
OPENROUTER_SITE_URL=http://localhost
OPENROUTER_APP_NAME=aerulias_ai
```

## Run

Run with a query:

```powershell
python agents/main.py "Explain machine learning in simple terms"
```

Run with a custom quality target and maximum rounds:

```powershell
python agents/main.py "Explain machine learning in simple terms" --target 90 --rounds 3
```

Run without memory:

```powershell
python agents/main.py "Explain machine learning in simple terms" --no-memory
```

Run with local sources for cited answers:

```powershell
python agents/main.py "Summarize my notes" --sources knowledge_base --target 85 --rounds 2
```

Or run interactively:

```powershell
python agents/main.py
```

## Dashboard

Start the local dashboard:

```powershell
python dashboard_server.py
```

Open:

```text
http://127.0.0.1:8000
```

The dashboard shows the query input, final answer, quality score, improvement rounds,
memory, run history, resume bullets, and a LinkedIn-ready project summary.

Turn on **Demo** mode in the dashboard when you want a safe presentation without API calls.

## FastAPI Backend

Start the production-style backend:

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

Deployment instructions are in:

```text
docs/deployment.md
```

## Test The Pipeline

```powershell
python test_pipeline.py
```

## Benchmark

Run the pipeline on multiple questions and create a score report:

```powershell
python benchmark.py --rounds 2 --target 90
```

The benchmark writes `benchmark_report.json` locally.

## Compare Models

```powershell
python compare_models.py "Explain machine learning simply" --models openai/gpt-4o-mini google/gemini-2.0-flash-001
```

The comparison writes `model_comparison.json` locally.

## Tests

```powershell
python -m unittest discover -s tests
```

## Resume And LinkedIn

See:

```text
docs/resume_linkedin.md
```

## Notes

- `.env` is ignored so API keys stay local.
- `memory_store.json` is ignored because it stores local learned lessons.
- `run_history.json` is ignored because it stores local execution history.
- `benchmark_report.json` is ignored because it stores local benchmark output.
- If you see `Connection error`, check your internet connection, OpenRouter key, and account credits.
