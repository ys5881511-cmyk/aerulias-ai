from agents.pipeline import run_pipeline
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json
import os


REPORT_PATH = Path(__file__).resolve().parent / "model_comparison.json"


def compare_models(query, models, rounds, target):
    original_model = os.environ.get("OPENROUTER_MODEL")
    results = []

    try:
        for model in models:
            print(f"Testing {model}")
            os.environ["OPENROUTER_MODEL"] = model
            result = run_pipeline(
                query,
                max_rounds=rounds,
                target_score=target,
                use_memory=False,
                save_outputs=False
            )

            results.append({
                "model": model,
                "final_score": result.get("final_score", 0),
                "rounds_used": len(result.get("rounds", [])),
                "final_answer": result.get("final_answer", "")
            })
    finally:
        if original_model is None:
            os.environ.pop("OPENROUTER_MODEL", None)
        else:
            os.environ["OPENROUTER_MODEL"] = original_model

    results.sort(key=lambda item: item["final_score"], reverse=True)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "target_score": target,
        "models": models,
        "winner": results[0] if results else None,
        "results": results
    }


def main():
    parser = argparse.ArgumentParser(description="Compare multiple OpenRouter models.")
    parser.add_argument("query", nargs="*", help="Query to test across models.")
    parser.add_argument("--models", nargs="+", default=[
        "openai/gpt-4o-mini",
        "google/gemini-2.0-flash-001"
    ])
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--target", type=int, default=85)
    args = parser.parse_args()

    query = " ".join(args.query).strip() or "Explain machine learning in simple terms"
    report = compare_models(query, args.models, args.rounds, args.target)
    REPORT_PATH.write_text(json.dumps(report, indent=2))

    print("\nModel comparison complete")
    print(f"Winner: {report['winner']['model'] if report['winner'] else 'none'}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
