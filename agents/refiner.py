import json
try:
    from .common import chat_json
except ImportError:
    from common import chat_json


def refine_answer(answer, issues, suggestions):
    prompt = f"""
You are an expert editor AI.

You will receive:
1. Original answer
2. Issues and suggestions

Your job:
- Improve the answer ONLY where needed
- Do not rewrite everything
- Fix logical errors
- Add missing parts

Return STRICT JSON:

{{
  "refined_answer": "...",
  "changes_made": [
    "change 1",
    "change 2"
  ]
}}

Original Answer:
{answer}

Issues:
{issues}

Suggestions:
{suggestions}
"""

    try:
        return chat_json(prompt, temperature=0.2)

    except json.JSONDecodeError:
        return {
            "refined_answer": answer,
            "changes_made": ["Refiner returned invalid JSON, so the original answer was kept."]
        }
    except Exception as error:
        return {
            "refined_answer": answer,
            "changes_made": [f"Refiner API failed: {error}"]
        }
