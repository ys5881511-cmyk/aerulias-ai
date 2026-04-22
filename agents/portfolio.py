def build_portfolio_summary(result):
    query = result.get("query", "a user query")
    final_score = result.get("final_score", 0)
    rounds = len(result.get("rounds", []))
    source_count = len(result.get("sources", []))
    memory_count = len(result.get("memory_used", []))

    resume_bullets = [
        "Built Aerulias AI, a multi-agent answer improvement system using Python, OpenRouter, and structured JSON pipelines.",
        f"Implemented generate-evaluate-refine loops with configurable target scores; latest demo reached a final score of {final_score}/100.",
        f"Added memory retrieval, source-grounded answering, run history, benchmarking, model comparison, tests, and an interactive dashboard."
    ]

    linkedin_post = (
        "I built Aerulias AI, a self-improving multi-agent answer system. "
        "Instead of accepting the first model response, it generates an answer, "
        "evaluates it for quality and hallucination risk, refines weak parts, "
        "and stores lessons in memory for future runs. "
        f"In my latest run, the system handled: \"{query}\" and completed "
        f"{rounds} improvement round(s) with a final score of {final_score}/100. "
        "This project helped me practice AI orchestration, prompt engineering, "
        "structured outputs, testing, and dashboard design."
    )

    beginner_explanation = (
        "Aerulias AI works like a student who checks their own homework. "
        "First it writes an answer. Then another agent grades the answer and "
        "points out problems. A third agent improves the answer using that feedback. "
        "The system can remember past mistakes, use local notes as sources, and show "
        "the full process in a dashboard."
    )

    return {
        "resume_bullets": resume_bullets,
        "linkedin_post": linkedin_post,
        "beginner_explanation": beginner_explanation,
        "stats": {
            "final_score": final_score,
            "rounds": rounds,
            "sources_used": source_count,
            "memories_used": memory_count
        }
    }
