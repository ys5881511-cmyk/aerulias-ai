from agents.pipeline import run_pipeline
from datetime import datetime, timezone
from pathlib import Path
import argparse
import json


DEFAULT_QUESTIONS = [
    "Explain artificial intelligence in simple terms.",
    "What are the advantages and disadvantages of online education?",
    "Explain photosynthesis to a 10 year old.",
    "What is the difference between supervised and unsupervised learning?",
    "How does the internet work in simple terms?"
]


REPORT_PATH = Path(__file__).resolve().parent / "benchmark_report.json"


def load_questions(path):
    if not path:
        return DEFAULT_QUESTIONS

    data = json.loads(Path(path).read_text())

    if isinstance(data, list):
        return [str(item) for item in data]

    return [str(item["query"]) for item in data.get("questions", [])]


def run_benchmark(questions, max_rounds, target_score):
    results = []

    for index, query in enumerate(questions, start=1):
        print(f"[{index}/{len(questions)}] {query}")
        result = run_pipeline(query, max_rounds=max_rounds, target_score=target_score)
        initial_score = result["rounds"][0]["evaluation"].get("score", 0) if result["rounds"] else 0
        final_score = result.get("final_score", 0)

        results.append({
            "query": query,
            "initial_score": initial_score,
            "final_score": final_score,
            "improvement": final_score - initial_score,
            "rounds_used": len(result.get("rounds", [])),
            "final_answer": result.get("final_answer", "")
        })

    average_initial = sum(item["initial_score"] for item in results) / len(results)
    average_final = sum(item["final_score"] for item in results) / len(results)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "question_count": len(results),
        "target_score": target_score,
        "max_rounds": max_rounds,
        "average_initial_score": round(average_initial, 2),
        "average_final_score": round(average_final, 2),
        "average_improvement": round(average_final - average_initial, 2),
        "results": results
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark the Aerulias AI pipeline.")
    parser.add_argument("--questions", help="Path to a JSON file containing benchmark questions.")
    parser.add_argument("--rounds", type=int, default=2)
    parser.add_argument("--target", type=int, default=90)
    args = parser.parse_args()

    questions = load_questions(args.questions)
    report = run_benchmark(questions, max_rounds=args.rounds, target_score=args.target)
    REPORT_PATH.write_text(json.dumps(report, indent=2))

    print("\nBenchmark complete")
    print(f"Questions: {report['question_count']}")
    print(f"Average initial score: {report['average_initial_score']}")
    print(f"Average final score: {report['average_final_score']}")
    print(f"Average improvement: {report['average_improvement']}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
