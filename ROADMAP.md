# Aerulias AI Roadmap

This project is being built as a self-improving multi-agent AI answer system.

## Current Prototype

- Generator agent creates an initial answer.
- Evaluator agent scores the answer and identifies weaknesses.
- Refiner agent improves the answer using evaluator feedback.
- Memory system saves useful lessons from past evaluations.
- Pipeline can run multiple refinement rounds until it reaches a target score.
- Run history is saved locally for analysis and demos.
- Web dashboard shows query, score, rounds, memory, and history.
- Benchmark runner measures score improvement across many questions.
- Demo mode supports presentations without API calls.
- Portfolio summaries generate resume bullets and LinkedIn-ready text.
- FastAPI backend supports production-style API routes and deployment.

## Next High-Impact Features

1. Better memory retrieval
   - Search only relevant past mistakes
   - Avoid adding repeated or low-quality memories
   - Store memory with timestamps and topics

2. Source-grounded answering
   - Add optional web/document retrieval
   - Require citations for factual answers
   - Reduce hallucination risk

3. Multi-model comparison
   - Run the same query through multiple models
   - Compare quality, latency, and cost
   - Pick the best answer automatically

4. Interview-ready engineering polish
   - Unit tests
   - Type hints
   - CI workflow
   - Architecture diagram
   - Clean demo video

5. Deployment
   - Host the dashboard online
   - Add a public demo mode
   - Add screenshots and a short walkthrough video

## Strong Project Pitch

Aerulias AI improves AI answers through a self-critical loop. It generates an answer,
evaluates it against quality criteria, refines weak parts, and stores lessons for future
runs. The goal is to make AI output more reliable, explainable, and continuously improving.
