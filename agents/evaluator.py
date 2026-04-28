"""Evaluator Agent: Scores and critiques answers for quality, correctness, and hallucination risk."""

import json
import logging
from typing import Any, Dict, Optional

try:
    from .common import chat_json
except ImportError:
    from common import chat_json

logger: logging.Logger = logging.getLogger(__name__)


def evaluate_answer(query: str, answer: str) -> Dict[str, Any]:
    """Evaluate an answer for quality, correctness, completeness, clarity, and hallucination risk.
    
    Args:
        query: Original user query (non-empty string).
        answer: Answer text to evaluate (non-empty string).
        
    Returns:
        Dictionary with structure:
        {
            "score": int (0-100),
            "issues": List[str],
            "improvement_suggestions": List[str]
        }
        Defaults to score=50 on parsing errors and score=0 on API errors.
        
    Raises:
        ValueError: If query or answer is empty.
    """
    # Input validation
    if not query or not isinstance(query, str):
        logger.warning("Invalid query provided to evaluator")
        return {
            "score": 0,
            "issues": ["Invalid query format"],
            "improvement_suggestions": ["Provide a valid string query"]
        }
    
    if not answer or not isinstance(answer, str):
        logger.warning("Invalid answer provided to evaluator")
        return {
            "score": 0,
            "issues": ["Invalid answer format"],
            "improvement_suggestions": ["Provide a valid string answer"]
        }
    
    prompt: str = """You are an expert evaluator AI.

Evaluate the answer based on:
1. Logical correctness
2. Completeness
3. Clarity
4. Hallucination risk

Return STRICT JSON only, with no additional text:

{
  "score": (0-100 integer),
  "issues": ["issue1", "issue2"],
  "improvement_suggestions": ["suggestion1", "suggestion2"]
}

Be strict and critical. Do not be lenient.

User Query:
{query}

AI Answer:
{answer}
""".format(query=query, answer=answer)

    try:
        logger.debug(f"Evaluating answer for query: {query[:50]}...")
        result: Dict[str, Any] = chat_json(prompt, temperature=0.2)
        
        # Validate response structure
        if not isinstance(result, dict):
            logger.error("Invalid response structure from chat_json")
            return {
                "score": 50,
                "issues": ["Invalid response format"],
                "improvement_suggestions": ["API returned invalid structure"]
            }
        
        # Validate score is in range
        score: int = result.get('score', 50)
        if not isinstance(score, int) or score < 0 or score > 100:
            logger.warning(f"Score out of range: {score}, clamping to 0-100")
            result['score'] = max(0, min(100, score))
        
        logger.info(f"Evaluation complete. Score: {result.get('score', 0)}")
        return result

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in evaluator: {e}", exc_info=True)
        return {
            "score": 50,
            "issues": ["Invalid JSON output from API"],
            "improvement_suggestions": ["API returned malformed JSON"]
        }
    except Exception as e:
        logger.error(f"Evaluator error: {type(e).__name__}: {e}", exc_info=True)
        return {
            "score": 0,
            "issues": [f"Evaluation failed: {type(e).__name__}"],
            "improvement_suggestions": ["Retry with a simpler query or answer"]
        }
