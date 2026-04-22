from pathlib import Path


SUPPORTED_EXTENSIONS = {".md", ".txt"}


def _source_files(paths):
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


def load_sources(paths, max_chars_per_source=3000):
    sources = []

    for index, path in enumerate(_source_files(paths), start=1):
        text = path.read_text(encoding="utf-8", errors="ignore").strip()

        if not text:
            continue

        sources.append({
            "id": f"S{index}",
            "title": path.name,
            "path": str(path),
            "text": text[:max_chars_per_source]
        })

    return sources


def format_source_context(sources):
    if not sources:
        return ""

    blocks = []

    for source in sources:
        blocks.append(
            f"[{source['id']}] {source['title']}\n{source['text']}"
        )

    return "\n\n".join(blocks)
