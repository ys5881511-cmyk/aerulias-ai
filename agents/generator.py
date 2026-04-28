"""Generator Agent: Creates initial answers from queries with memory and source context."""

import json
import logging
from typing import Any, Dict

try:
    from .common import chat_json
except ImportError:
    from common import chat_json

logger = logging.getLogger(__name__)


def _normalize_answer(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize and validate confidence score to 0-100 range.
    
    Args:
        data: Dictionary containing answer data with confidence field.
        
    Returns:
        Dictionary with normalized confidence score (0-100).
    """
    confidence = data.get("confidence", 0)

    if isinstance(confidence, float) and 0 <= confidence <= 1:
        confidence = round(confidence * 100)

    try:
        confidence = int(confidence)
    except (TypeError, ValueError):
        logger.warning(f"Invalid confidence value: {confidence}, defaulting to 0")
        confidence = 0

    data["confidence"] = max(0, min(100, confidence))
    return data


def generate_answer(query: str, memory_context: str = "", source_context: str = "") -> Dict[str, Any]:
    """Generate an initial answer to a query using optional memory and source context.
    
    Args:
        query: User question to answer.
        memory_context: Optional formatted context from past mistakes.
        source_context: Optional formatted context from source documents.
        
    Returns:
        Dictionary with 'answer', 'reasoning', and 'confidence' fields.
        Confidence is normalized to 0-100 range.
        
    Raises:
        Gracefully handles API and parsing errors by returning fallback response.
    """
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
        logger.debug(f"Generating answer for query: {query[:50]}...")
        data = chat_json(prompt, temperature=0.2)
        result = _normalize_answer(data)
        logger.info(f"Successfully generated answer with confidence: {result.get('confidence', 0)}")
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in generator: {e}")
        return {
            "answer": "The model returned invalid JSON.",
            "reasoning": "Parsing failed",
            "confidence": 50
        }
    except Exception as error:
        logger.error(f"Generator error: {error}", exc_info=True)
        return {
            "answer": "The model request failed.",
            "reasoning": str(error),
            "confidence": 0
        }
