"""Pipeline Orchestrator: Coordinates multi-round generate-evaluate-refine loops."""

import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

try:
    from .generator import generate_answer
    from .evaluator import evaluate_answer
    from .refiner import refine_answer
    from .memory import find_relevant_memory, format_memory_context, save_memory
    from .sources import format_source_context, load_sources
    from .portfolio import build_portfolio_summary
    from .demo import build_demo_result
except ImportError:
    from generator import generate_answer
    from evaluator import evaluate_answer
    from refiner import refine_answer
    from memory import find_relevant_memory, format_memory_context, save_memory
    from sources import format_source_context, load_sources
    from portfolio import build_portfolio_summary
    from demo import build_demo_result
import json

logger = logging.getLogger(__name__)

RUN_HISTORY_PATH = Path(__file__).resolve().parent.parent / "run_history.json"


def _load_run_history() -> List[Dict[str, Any]]:
    """Load run history from persistent storage.
    
    Returns:
        List of previous pipeline run results, or empty list if file doesn't exist.
    """
    if not RUN_HISTORY_PATH.exists():
        logger.debug("Run history file does not exist yet")
        return []

    try:
        history = json.loads(RUN_HISTORY_PATH.read_text())
        logger.info(f"Loaded {len(history)} previous runs")
        return history
    except json.JSONDecodeError:
        logger.error(f"Run history file corrupted: {RUN_HISTORY_PATH}")
        return []


def save_run(result: Dict[str, Any]) -> None:
    """Save a pipeline run result to history.
    
    Args:
        result: Complete pipeline result dictionary to save.
    """
    try:
        history = _load_run_history()
        history.append(result)
        RUN_HISTORY_PATH.write_text(json.dumps(history, indent=2))
        logger.info(f"Saved run result. Total runs: {len(history)}")
    except Exception as e:
        logger.error(f"Failed to save run: {e}", exc_info=True)


def run_pipeline(
    query: str,
    max_rounds: int = 2,
    target_score: int = 90,
    use_memory: bool = True,
    source_paths: Optional[List[str]] = None,
    save_outputs: bool = True,
    demo_mode: bool = False
) -> Dict[str, Any]:
    """Execute complete multi-round answer improvement pipeline.
    
    Generates initial answer, evaluates it, refines it based on feedback,
    and repeats until target score is reached or max rounds exceeded.
    
    Args:
        query: User question to answer.
        max_rounds: Maximum refinement iterations (1-5).
        target_score: Target quality score to stop at (0-100).
        use_memory: Whether to use past mistakes for context.
        source_paths: Optional list of paths to source documents.
        save_outputs: Whether to save results to history and memory.
        demo_mode: Use demo results without API calls.
        
    Returns:
        Dictionary with complete pipeline results including query, rounds,
        final_answer, final_score, portfolio recommendations, and metadata.
        
    Note:
        Results are automatically saved to run_history.json if save_outputs=True.
    """
    if demo_mode:
        logger.info("Running in demo mode")
        result = build_demo_result(
            query,
            max_rounds=max_rounds,
            target_score=target_score,
            use_memory=use_memory,
            source_paths=source_paths
        )

        if save_outputs:
            save_run(result)

        return result

    logger.info(f"Starting pipeline run. Query: {query[:50]}... Max rounds: {max_rounds}, Target: {target_score}")
    
    relevant_memory = find_relevant_memory(query) if use_memory else []
    memory_context = format_memory_context(relevant_memory) if use_memory else ""
    sources = load_sources(source_paths or [])
    source_context = format_source_context(sources)
    
    logger.debug(f"Memory items: {len(relevant_memory)}, Sources: {len(sources)}")
    
    generated = generate_answer(
        query,
        memory_context=memory_context,
        source_context=source_context
    )

    rounds = []
    current_answer = generated["answer"]

    for round_number in range(1, max_rounds + 1):
        logger.info(f"Starting round {round_number}/{max_rounds}")
        
        evaluation = evaluate_answer(query, current_answer)
        refined = refine_answer(
            current_answer,
            evaluation["issues"],
            evaluation["improvement_suggestions"]
        )

        rounds.append({
            "round": round_number,
            "answer_before_refinement": current_answer,
            "evaluation": evaluation,
            "refinement": refined
        })

        current_score = evaluation.get("score", 0)
        logger.info(f"Round {round_number} complete. Score: {current_score}")
        
        if current_score >= target_score:
            logger.info(f"Target score {target_score} reached! Stopping pipeline.")
            break

        current_answer = refined["refined_answer"]

    final_evaluation = rounds[-1]["evaluation"] if rounds else {}

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "target_score": target_score,
        "max_rounds": max_rounds,
        "sources": [{"id": source["id"], "title": source["title"], "path": source["path"]} for source in sources],
        "memory_used": relevant_memory,
        "generated": generated,
        "rounds": rounds,
        "final_answer": rounds[-1]["refinement"]["refined_answer"] if rounds else generated["answer"],
        "final_score": final_evaluation.get("score", 0)
    }
    result["portfolio"] = build_portfolio_summary(result)

    logger.info(f"Pipeline complete. Final score: {result['final_score']}/{target_score}. Rounds used: {len(rounds)}")
    
    if save_outputs:
        save_memory(query, final_evaluation)
        save_run(result)
        logger.info("Results saved to history and memory")

    return result
