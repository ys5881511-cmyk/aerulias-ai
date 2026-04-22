import json
import re
from pathlib import Path


MEMORY_PATH = Path(__file__).resolve().parent.parent / "memory_store.json"
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "for", "from", "how", "in",
    "is", "it", "of", "on", "or", "that", "the", "this", "to", "what",
    "when", "where", "which", "why", "with"
}


def load_memory():
    if not MEMORY_PATH.exists():
        return []

    try:
        return json.loads(MEMORY_PATH.read_text())
    except json.JSONDecodeError:
        return []


def tokenize(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return {word for word in words if word not in STOP_WORDS and len(word) > 2}


def find_relevant_memory(query, limit=5):
    query_tokens = tokenize(query)

    if not query_tokens:
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
    return [item for _, item in scored_items[:limit]]


def format_memory_context(memory_items):
    if not memory_items:
        return "No past mistakes recorded yet."

    lines = []

    for index, item in enumerate(memory_items[-5:], start=1):
        query = item.get("query", "Unknown query")
        issues = "; ".join(item.get("issues", []))
        suggestions = "; ".join(item.get("improvement_suggestions", []))
        lines.append(f"{index}. Query: {query}\nIssues: {issues}\nLessons: {suggestions}")

    return "\n\n".join(lines)


def save_memory(query, evaluation):
    issues = evaluation.get("issues", [])
    suggestions = evaluation.get("improvement_suggestions", [])

    if "Connection error." in issues or "API failed" in suggestions:
        return

    memory_items = load_memory()

    memory_items.append({
        "query": query,
        "score": evaluation.get("score", 0),
        "issues": issues,
        "improvement_suggestions": suggestions
    })

    MEMORY_PATH.write_text(json.dumps(memory_items, indent=2))
