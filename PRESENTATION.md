# Presentation Guide

## Project Title

Aerulias AI: A Self-Improving Multi-Agent Answer System

## One-Minute Explanation

Aerulias AI is a Python project that improves AI answers using multiple specialized agents.
Instead of trusting the first answer, the system generates an answer, evaluates it, refines
weak parts, and stores lessons from past mistakes. This creates a feedback loop that makes
future answers more reliable and explainable.

## Architecture

```text
User Query
   |
   v
Memory Retrieval
   |
   v
Generator Agent
   |
   v
Evaluator Agent
   |
   v
Refiner Agent
   |
   v
Quality Loop
   |
   v
Final Answer + Run History + Memory Update
```

## Demo Command

```powershell
python agents/main.py "Explain artificial intelligence in simple terms" --target 90 --rounds 3
```

## What To Show

1. The generated first answer.
2. The evaluator score, issues, and improvement suggestions.
3. The refined answer after feedback.
4. The final score and run history.
5. The memory file showing that the system learns lessons from previous runs.

## Best Talking Points

- Multi-agent design: each agent has a focused responsibility.
- Structured JSON: agents communicate in predictable machine-readable outputs.
- Self-improvement loop: answers are evaluated and refined instead of accepted blindly.
- Memory: the system stores previous weaknesses and applies them later.
- OpenRouter integration: the project can switch models through configuration.
- Engineering quality: environment variables, shared client helpers, CLI options, docs, and roadmap.
- Source-grounding: local notes can be used as cited evidence.
- Benchmarking: the system can measure score improvement across questions.
- Model comparison: multiple OpenRouter models can be compared on the same query.

## Future Scope

- FastAPI backend.
- Automated tests and CI.
