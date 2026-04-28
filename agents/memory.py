"""Memory System: Stores and retrieves past mistakes and lessons for self-improvement."""

import json
import re
import logging
from pathlib import Path
from typing import Any, Dict, List, Set

logger = logging.getLogger(__name__)

MEMORY_PATH = Path(__file__).resolve().parent.parent / "memory_store.json"
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "for", "from", "how", "in",
    "is", "it", "of", "on", "or", "that", "the", "this", "to", "what",
    "when", "where", "which", "why", "with"
}


def load_memory() -> List[Dict[str, Any]]:
    """Load memory items from persistent storage.
    
    Returns:
        List of memory dictionaries, or empty list if file doesn't exist or is corrupted.
    """
    if not MEMORY_PATH.exists():
        logger.debug("Memory file does not exist yet")
        return []

    try:
        memory_items = json.loads(MEMORY_PATH.read_text())
        logger.info(f"Loaded {len(memory_items)} memory items")
        return memory_items
    except json.JSONDecodeError:
        logger.error(f"Memory file corrupted: {MEMORY_PATH}")
        return []


def tokenize(text: str) -> Set[str]:
    """Tokenize text into meaningful words, filtering stopwords.
    
    Args:
        text: Input text to tokenize.
        
    Returns:
        Set of tokens (words) with length > 2, excluding stopwords.
    """
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return {word for word in words if word not in STOP_WORDS and len(word) > 2}


def find_relevant_memory(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Find memory items relevant to the current query using token overlap.
    
    Args:
        query: User query to match against past queries.
        limit: Maximum number of memory items to return.
        
    Returns:
        List of most relevant memory items, sorted by relevance score.
    """
    query_tokens = tokenize(query)

    if not query_tokens:
        logger.debug("Query has no meaningful tokens, returning recent memories")
        return load_memory()[-limit:]

    scored_items = []

    for item in load_memory():
        memory_text = " ".join([
            item.get("query", ""),
            " ".join(item.get("issues", [])),
            " ".join(item.get("improvement_suggestions", []))
        ])
        memory_tokens = tokenize(memory_text)
        overlap = len(query_tokens & memory_tokens)

        if overlap:
            scored_items.append((overlap, item))

    scored_items.sort(key=lambda pair: pair[0], reverse=True)
    result = [item for _, item in scored_items[:limit]]
    logger.debug(f"Found {len(result)} relevant memory items for query")
    return result


def format_memory_context(memory_items: List[Dict[str, Any]]) -> str:
    """Format memory items into a readable context string for the generator.
    
    Args:
        memory_items: List of memory dictionaries to format.
        
    Returns:
        Formatted string with past mistakes and lessons, or "No past mistakes..." if empty.
    """
    if not memory_items:
        return "No past mistakes recorded yet."

    lines = []

    for index, item in enumerate(memory_items[-5:], start=1):
        query = item.get("query", "Unknown query")
        issues = "; ".join(item.get("issues", []))
        suggestions = "; ".join(item.get("improvement_suggestions", []))
        lines.append(f"{index}. Query: {query}\nIssues: {issues}\nLessons: {suggestions}")

    return "\n\n".join(lines)


def save_memory(query: str, evaluation: Dict[str, Any]) -> None:
    """Save evaluation results to memory for future reference.
    
    Args:
        query: Original user query.
        evaluation: Evaluation dictionary with score, issues, and suggestions.
        
    Note:
        Skips saving if evaluation indicates an API error.
    """
    issues = evaluation.get("issues", [])
    suggestions = evaluation.get("improvement_suggestions", [])

    # Skip saving API errors
    if "Connection error." in issues or "API failed" in suggestions:
        logger.warning("Skipping memory save due to API error")
        return

    try:
        memory_items = load_memory()

        memory_items.append({
            "query": query,
            "score": evaluation.get("score", 0),
            "issues": issues,
            "improvement_suggestions": suggestions
        })

        MEMORY_PATH.write_text(json.dumps(memory_items, indent=2))
        logger.info(f"Saved memory item. Total memories: {len(memory_items)}")
    except Exception as e:
        logger.error(f"Failed to save memory: {e}", exc_info=True)
