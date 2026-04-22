import unittest
from pathlib import Path

from agents.sources import format_source_context, load_sources


class SourceTests(unittest.TestCase):
    def test_load_sources_reads_text_files(self):
        temp_dir = Path.cwd() / ".test_tmp_sources"
        temp_dir.mkdir(exist_ok=True)
        path = temp_dir / "note.md"

        try:
            path.write_text("Aerulias source text", encoding="utf-8")

            sources = load_sources([str(path)])

            self.assertEqual(len(sources), 1)
            self.assertEqual(sources[0]["id"], "S1")
            self.assertIn("Aerulias", sources[0]["text"])
        finally:
            if path.exists():
                path.unlink()
            if temp_dir.exists():
                temp_dir.rmdir()

    def test_format_source_context_includes_ids(self):
        context = format_source_context([
            {"id": "S1", "title": "doc.md", "text": "Example text"}
        ])

        self.assertIn("[S1] doc.md", context)
        self.assertIn("Example text", context)


if __name__ == "__main__":
    unittest.main()
