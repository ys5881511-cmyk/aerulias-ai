import json
try:
    from .common import chat_json
except ImportError:
    from common import chat_json


def _normalize_answer(data):
    confidence = data.get("confidence", 0)

    if isinstance(confidence, float) and 0 <= confidence <= 1:
        confidence = round(confidence * 100)

    try:
        confidence = int(confidence)
    except (TypeError, ValueError):
        confidence = 0

    data["confidence"] = max(0, min(100, confidence))
    return data


def generate_answer(query, memory_context="", source_context=""):
    if memory_context:
        prompt = f"""
You are an AI system with memory of past mistakes.

Here are past mistakes and lessons:
{memory_context}

Before answering:
- Check if similar mistake exists
- Avoid repeating errors
- Apply learned improvements

Now answer the query carefully:

{query}

Return response strictly in JSON format:
{{
  "answer": "...",
  "reasoning": "...",
  "confidence": (0-100)
}}
"""
    else:
        prompt = f"""
You are an expert AI assistant.

Your task is to answer the user query with:
1. Clear reasoning
2. Complete and accurate explanation
3. Structured output

Return response strictly in JSON format:
{{
  "answer": "...",
  "reasoning": "...",
  "confidence": (0-100)
}}

Guidelines:
- Do not hallucinate facts
- If unsure, mention uncertainty
- Be logically consistent
- Cover all parts of the question

User Query:
{query}
"""

    if source_context:
        prompt += f"""

Source-grounding requirements:
- Use the provided sources when they are relevant.
- Cite source-backed claims inline using source IDs like [S1].
- If the sources do not contain enough evidence, say what is uncertain.
- Do not invent citations.

Sources:
{source_context}
"""

    try:
        data = chat_json(prompt, temperature=0.2)
        return _normalize_answer(data)
    except json.JSONDecodeError:
        return {
            "answer": "The model returned invalid JSON.",
            "reasoning": "Parsing failed",
            "confidence": 50
        }
    except Exception as error:
        return {
            "answer": "The model request failed.",
            "reasoning": str(error),
            "confidence": 0
        }
