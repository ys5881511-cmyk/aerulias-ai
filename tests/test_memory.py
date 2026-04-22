import unittest

from agents.memory import find_relevant_memory, format_memory_context, tokenize
import agents.memory as memory


class MemoryTests(unittest.TestCase):
    def test_tokenize_removes_common_words(self):
        self.assertEqual(tokenize("What is the AI system?"), {"system"})

    def test_format_memory_context_empty(self):
        self.assertEqual(format_memory_context([]), "No past mistakes recorded yet.")

    def test_find_relevant_memory_uses_query_overlap(self):
        original_load_memory = memory.load_memory
        memory.load_memory = lambda: [
            {
                "query": "Explain machine learning",
                "score": 70,
                "issues": ["Missing examples"],
                "improvement_suggestions": ["Add examples"]
            },
            {
                "query": "Explain photosynthesis",
                "score": 80,
                "issues": ["Too technical"],
                "improvement_suggestions": ["Use simple language"]
            }
        ]

        try:
            result = find_relevant_memory("machine learning examples", limit=1)
            self.assertEqual(result[0]["query"], "Explain machine learning")
        finally:
            memory.load_memory = original_load_memory


if __name__ == "__main__":
    unittest.main()
