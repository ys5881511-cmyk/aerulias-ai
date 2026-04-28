"""Refiner Agent: Improves answers based on evaluator feedback without unnecessary rewrites."""

import json
import logging
from typing import Any, Dict, List

try:
    from .common import chat_json
except ImportError:
    from common import chat_json

logger = logging.getLogger(__name__)


def refine_answer(answer: str, issues: List[str], suggestions: List[str]) -> Dict[str, Any]:
    """Refine an answer based on evaluator feedback with targeted improvements.
    
    Args:
        answer: Original answer text to refine.
        issues: List of identified problems from evaluation.
        suggestions: List of improvement suggestions from evaluation.
        
    Returns:
        Dictionary with 'refined_answer' and 'changes_made' list.
        Falls back to original answer on errors with explanation.
    """
    prompt = """You are an expert editor AI.

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
        logger.debug(f"Refining answer. Issues: {len(issues)}, Suggestions: {len(suggestions)}")
        result = chat_json(prompt, temperature=0.2)
        logger.info(f"Refinement complete. Changes made: {len(result.get('changes_made', []))}")
        return result

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in refiner: {e}")
        return {
            "refined_answer": answer,
            "changes_made": ["Refiner returned invalid JSON, so the original answer was kept."]
        }
    except Exception as error:
        logger.error(f"Refiner error: {error}", exc_info=True)
        return {
            "refined_answer": answer,
            "changes_made": [f"Refiner API failed: {error}"]
        }
