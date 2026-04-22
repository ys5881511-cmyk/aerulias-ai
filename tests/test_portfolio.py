import unittest

from agents.demo import build_demo_result
from agents.portfolio import build_portfolio_summary


class PortfolioTests(unittest.TestCase):
    def test_portfolio_summary_contains_resume_bullets(self):
        result = {
            "query": "Explain AI",
            "final_score": 91,
            "rounds": [{"round": 1}],
            "sources": [],
            "memory_used": []
        }

        summary = build_portfolio_summary(result)

        self.assertIn("resume_bullets", summary)
        self.assertGreaterEqual(len(summary["resume_bullets"]), 3)
        self.assertIn("LinkedIn", "LinkedIn Draft")

    def test_demo_result_never_calls_api(self):
        result = build_demo_result("Explain AI", max_rounds=2, target_score=90)

        self.assertTrue(result["demo_mode"])
        self.assertIn("portfolio", result)
        self.assertGreaterEqual(result["final_score"], 90)


if __name__ == "__main__":
    unittest.main()
