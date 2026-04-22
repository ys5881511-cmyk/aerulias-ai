import unittest

from agents.generator import _normalize_answer


class GeneratorTests(unittest.TestCase):
    def test_normalize_confidence_percentage_float(self):
        data = _normalize_answer({"answer": "x", "reasoning": "y", "confidence": 0.92})
        self.assertEqual(data["confidence"], 92)

    def test_normalize_confidence_clamps_large_number(self):
        data = _normalize_answer({"answer": "x", "reasoning": "y", "confidence": 200})
        self.assertEqual(data["confidence"], 100)


if __name__ == "__main__":
    unittest.main()
