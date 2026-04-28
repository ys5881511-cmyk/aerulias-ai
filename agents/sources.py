"""Source Loader: Loads and formats documents for source-grounded answering."""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS: Set[str] = {".md", ".txt"}


def _source_files(paths: Optional[List[str]]) -> List[Path]:
    """Find all supported source files from given paths.
    
    Args:
        paths: List of file or directory paths to search.
        
    Returns:
        List of Path objects for all supported source files found.
    """
    files = []

    for raw_path in paths or []:
        path = Path(raw_path).resolve()

        if path.is_dir():
            files.extend(
                item for item in sorted(path.rglob("*"))
                if item.suffix.lower() in SUPPORTED_EXTENSIONS and item.is_file()
            )
        elif path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path)

    return files


def load_sources(paths: Optional[List[str]], max_chars_per_source: int = 3000) -> List[Dict[str, str]]:
    """Load source documents from file or directory paths.
    
    Args:
        paths: List of .md or .txt file/directory paths to load.
        max_chars_per_source: Maximum characters to include per source.
        
    Returns:
        List of source dictionaries with id, title, path, and text fields.
    """
    sources = []

    for index, path in enumerate(_source_files(paths), start=1):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore").strip()

            if not text:
                logger.debug(f"Skipping empty source: {path.name}")
                continue

            sources.append({
                "id": f"S{index}",
                "title": path.name,
                "path": str(path),
                "text": text[:max_chars_per_source]
            })
        except Exception as e:
            logger.warning(f"Failed to load source {path}: {e}")

    logger.info(f"Loaded {len(sources)} sources")
    return sources


def format_source_context(sources: List[Dict[str, str]]) -> str:
    """Format source documents into context string for generator.
    
    Args:
        sources: List of source dictionaries from load_sources().
        
    Returns:
        Formatted string with all sources, or empty string if no sources.
    """
    if not sources:
        return ""

    blocks = []

    for source in sources:
        blocks.append(
            f"[{source['id']}] {source['title']}\n{source['text']}"
        )

    return "\n\n".join(blocks)
