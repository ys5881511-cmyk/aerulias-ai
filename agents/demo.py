from datetime import datetime, timezone

try:
    from .portfolio import build_portfolio_summary
except ImportError:
    from portfolio import build_portfolio_summary


def build_demo_result(query, max_rounds=2, target_score=90, use_memory=True, source_paths=None):
    generated = {
        "answer": (
            "Machine learning is a way for computers to learn patterns from data "
            "and use those patterns to make predictions or decisions."
        ),
        "reasoning": (
            "The answer uses simple language and avoids technical details first, "
            "so a beginner can understand the main idea."
        ),
        "confidence": 88
    }

    first_refined = (
        "Machine learning is a way for computers to learn from examples instead "
        "of being given exact instructions for every situation. For example, a "
        "movie app can learn what you like by looking at movies you watched before."
    )

    final_refined = (
        "Machine learning is a way for computers to learn from examples instead "
        "of being given exact instructions for every situation. Think of it like "
        "teaching a student with practice questions. A movie app, for example, can "
        "study what you watched before and recommend similar movies. The system does "
        "not understand like a human, but it finds patterns in data and improves as "
        "it sees more examples."
    )

    rounds = [
        {
            "round": 1,
            "answer_before_refinement": generated["answer"],
            "evaluation": {
                "score": 78,
                "issues": [
                    "The answer is correct but too short for a beginner.",
                    "It needs a simple real-world example."
                ],
                "improvement_suggestions": [
                    "Add an analogy.",
                    "Add a familiar example such as recommendations."
                ]
            },
            "refinement": {
                "refined_answer": first_refined,
                "changes_made": [
                    "Added beginner-friendly wording.",
                    "Added a movie recommendation example."
                ]
            }
        }
    ]

    if max_rounds > 1 and target_score > 85:
        rounds.append({
            "round": 2,
            "answer_before_refinement": first_refined,
            "evaluation": {
                "score": 92,
                "issues": [
                    "The answer should clarify that machines do not understand like humans."
                ],
                "improvement_suggestions": [
                    "Add one sentence about pattern recognition instead of human understanding."
                ]
            },
            "refinement": {
                "refined_answer": final_refined,
                "changes_made": [
                    "Added a practice-question analogy.",
                    "Clarified that machine learning finds patterns rather than human-like understanding."
                ]
            }
        })

    final_score = rounds[-1]["evaluation"]["score"]

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "target_score": target_score,
        "max_rounds": max_rounds,
        "demo_mode": True,
        "sources": [{"id": "S1", "title": "demo_source.md", "path": "demo"}] if source_paths else [],
        "memory_used": [
            {
                "query": "Explain AI simply",
                "score": 82,
                "issues": ["Needed simpler examples."],
                "improvement_suggestions": ["Use everyday analogies."]
            }
        ] if use_memory else [],
        "generated": generated,
        "rounds": rounds,
        "final_answer": rounds[-1]["refinement"]["refined_answer"],
        "final_score": final_score
    }
    result["portfolio"] = build_portfolio_summary(result)
    return result
