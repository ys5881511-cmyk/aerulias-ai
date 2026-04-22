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
from pathlib import Path
from datetime import datetime, timezone
import json


RUN_HISTORY_PATH = Path(__file__).resolve().parent.parent / "run_history.json"


def _load_run_history():
    if not RUN_HISTORY_PATH.exists():
        return []

    try:
        return json.loads(RUN_HISTORY_PATH.read_text())
    except json.JSONDecodeError:
        return []


def save_run(result):
    history = _load_run_history()
    history.append(result)
    RUN_HISTORY_PATH.write_text(json.dumps(history, indent=2))


def run_pipeline(
    query,
    max_rounds=2,
    target_score=90,
    use_memory=True,
    source_paths=None,
    save_outputs=True,
    demo_mode=False
):
    if demo_mode:
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

    relevant_memory = find_relevant_memory(query) if use_memory else []
    memory_context = format_memory_context(relevant_memory) if use_memory else ""
    sources = load_sources(source_paths or [])
    source_context = format_source_context(sources)
    generated = generate_answer(
        query,
        memory_context=memory_context,
        source_context=source_context
    )

    rounds = []
    current_answer = generated["answer"]

    for round_number in range(1, max_rounds + 1):
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

        if evaluation.get("score", 0) >= target_score:
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

    if save_outputs:
        save_memory(query, final_evaluation)
        save_run(result)

    return result
