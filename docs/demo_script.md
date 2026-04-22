# Demo Script

## Opening

My project is called Aerulias AI. It is a self-improving multi-agent answer system. Instead of accepting the first AI answer, it generates an answer, evaluates it, refines weak parts, and stores lessons in memory for future runs.

## Demo 1: Command Line Pipeline

Run:

```powershell
python agents/main.py "Explain artificial intelligence in simple terms" --target 90 --rounds 3
```

Explain:

1. The generator creates the first answer.
2. The evaluator gives a score and identifies weaknesses.
3. The refiner improves the answer.
4. The loop can repeat until it reaches the target score.

## Demo 2: Dashboard

Run:

```powershell
python dashboard_server.py
```

Open:

```text
http://127.0.0.1:8000
```

Show:

1. Query input.
2. Target score and rounds.
3. Final score dial.
4. Improvement rounds.
5. Memory and history panels.

## Demo 3: Source-Grounded Answer

Create a folder called `knowledge_base` and add a `.md` or `.txt` file with factual notes.

Run:

```powershell
python agents/main.py "Answer using my notes" --sources knowledge_base --target 85 --rounds 2
```

Explain that the system can cite local sources using IDs like `[S1]`.

## Demo 4: Benchmark

Run:

```powershell
python benchmark.py --rounds 2 --target 90
```

Explain that the project measures quality improvement across multiple questions.

## Demo 5: Model Comparison

Run:

```powershell
python compare_models.py "Explain machine learning simply" --models openai/gpt-4o-mini google/gemini-2.0-flash-001
```

Explain that the system can compare models by final answer score.

## Closing

The main idea is reliability. Aerulias AI does not blindly trust a model response. It creates a feedback loop around generation, evaluation, refinement, memory, and measurement.
