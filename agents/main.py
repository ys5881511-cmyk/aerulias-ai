"""Main CLI entry point for running the Aerulias AI pipeline."""

import logging
from typing import List, Optional

try:
    from .pipeline import run_pipeline
except ImportError:
    from pipeline import run_pipeline
import argparse
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse and return command-line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
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
    try:
        args = parse_args()
        query = " ".join(args.query).strip() or input("Enter your query: ").strip()
     
        if not query:
            logger.error("Please enter a query.")
        else:
            logger.info(f"Starting pipeline with query: {query[:60]}...")
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
            logger.info("Pipeline execution completed successfully")
    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise

