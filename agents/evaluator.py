import json
try:
    from .common import chat_json
except ImportError:
    from common import chat_json


def evaluate_answer(query, answer):
    prompt = f"""
You are an expert evaluator AI.

Evaluate the answer based on:
1. Logical correctness
2. Completeness
3. Clarity
4. Hallucination risk

Return STRICT JSON:

{{
  "score": (0-100),
  "issues": ["issue1", "issue2"],
  "improvement_suggestions": ["suggestion1", "suggestion2"]
}}

Be strict and critical. Do not be lenient.

User Query:
{query}

AI Answer:
{answer}
"""

    try:
        return chat_json(prompt, temperature=0.2)

    except json.JSONDecodeError:
        return {
            "score": 50,
            "issues": ["Invalid JSON output"],
            "improvement_suggestions": ["Fix formatting"]
        }
    except Exception as e:
        return {
            "score": 0,
            "issues": [str(e)],
            "improvement_suggestions": ["API failed"]
        }
