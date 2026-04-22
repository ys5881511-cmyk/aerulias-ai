try:
    from .pipeline import run_pipeline
except ImportError:
    from pipeline import run_pipeline
import argparse
import json


def parse_args():
    parser = argparse.ArgumentParser(description="Run the Aerulias AI improvement pipeline.")
    parser.add_argument("query", nargs="*", help="User query to answer.")
    parser.add_argument("--rounds", type=int, default=2, help="Maximum refinement rounds.")
    parser.add_argument("--target", type=int, default=90, help="Target evaluation score.")
    parser.add_argument("--no-memory", action="store_true", help="Disable memory context for this run.")
    parser.add_argument("--sources", nargs="*", help="Optional .txt/.md files or folders for cited answers.")
    parser.add_argument("--no-save", action="store_true", help="Do not save memory or run history.")
    parser.add_argument("--demo", action="store_true", help="Run without API calls using a polished demo result.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    query = " ".join(args.query).strip() or input("Enter your query: ").strip()
 
    if not query:
        print("Please enter a query.")
    else:
        result = run_pipeline(
            query,
            max_rounds=args.rounds,
            target_score=args.target,
            use_memory=not args.no_memory,
            source_paths=args.sources,
            save_outputs=not args.no_save,
            demo_mode=args.demo
        )
        print(json.dumps(result, indent=2))
