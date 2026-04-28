"""Unit tests for Aerulias AI agent components.

Tests cover generator, evaluator, refiner, and memory functions
with mocked API calls to ensure fast, deterministic test execution.
"""

import pytest
import json
import logging
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
import tempfile

# Add agents directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))

from generator import generate_answer, _normalize_answer
from evaluator import evaluate_answer
from refiner import refine_answer
from memory import load_memory, tokenize, find_relevant_memory, format_memory_context, save_memory

logger = logging.getLogger(__name__)


class TestNormalizeAnswer:
    """Test answer normalization and confidence scoring."""

    def test_normalize_answer_with_float_confidence(self) -> None:
        """Test that float confidence (0-1) is converted to 0-100 scale."""
        data = {"answer": "test", "confidence": 0.85}
        result = _normalize_answer(data)
        assert result["confidence"] == 85

    def test_normalize_answer_with_int_confidence(self) -> None:
        """Test that integer confidence is clamped to 0-100."""
        data = {"answer": "test", "confidence": 95}
        result = _normalize_answer(data)
        assert result["confidence"] == 95

    def test_normalize_answer_clamps_above_100(self) -> None:
        """Test that confidence > 100 is clamped to 100."""
        data = {"answer": "test", "confidence": 150}
        result = _normalize_answer(data)
        assert result["confidence"] == 100

    def test_normalize_answer_clamps_below_0(self) -> None:
        """Test that confidence < 0 is clamped to 0."""
        data = {"answer": "test", "confidence": -10}
        result = _normalize_answer(data)
        assert result["confidence"] == 0

    def test_normalize_answer_handles_invalid_confidence(self) -> None:
        """Test that invalid confidence values default to 0."""
        data = {"answer": "test", "confidence": "invalid"}
        result = _normalize_answer(data)
        assert result["confidence"] == 0

    def test_normalize_answer_missing_confidence(self) -> None:
        """Test that missing confidence defaults to 0."""
        data = {"answer": "test"}
        result = _normalize_answer(data)
        assert result["confidence"] == 0


class TestGenerateAnswer:
    """Test answer generation with mocked API calls."""

    @patch("common.chat_json")
    def test_generate_answer_basic(self, mock_chat_json: MagicMock) -> None:
        """Test basic answer generation."""
        mock_chat_json.return_value = {
            "answer": "Machine learning is...",
            "reasoning": "...",
            "confidence": 0.9
        }
        
        result = generate_answer("Explain ML")
        
        assert result["answer"] == "Machine learning is..."
        assert result["confidence"] == 90
        mock_chat_json.assert_called_once()

    @patch("common.chat_json")
    def test_generate_answer_with_memory_context(self, mock_chat_json: MagicMock) -> None:
        """Test answer generation with memory context."""
        mock_chat_json.return_value = {
            "answer": "Improved answer",
            "reasoning": "Used memory",
            "confidence": 85
        }
        
        result = generate_answer("Explain ML", memory_context="Past lesson: be clear")
        
        assert "memory_context" not in result  # Memory affects prompt, not result
        assert result["confidence"] == 85

    @patch("common.chat_json")
    def test_generate_answer_with_source_context(self, mock_chat_json: MagicMock) -> None:
        """Test answer generation with source documents."""
        mock_chat_json.return_value = {
            "answer": "According to sources...",
            "reasoning": "Source-backed",
            "confidence": 92
        }
        
        result = generate_answer("Explain ML", source_context="[S1] ML is...")
        
        assert result["confidence"] == 92
        mock_chat_json.assert_called_once()

    @patch("common.chat_json")
    def test_generate_answer_handles_json_error(self, mock_chat_json: MagicMock) -> None:
        """Test graceful handling of JSON parsing errors."""
        mock_chat_json.side_effect = json.JSONDecodeError("msg", "doc", 0)
        
        result = generate_answer("Explain ML")
        
        assert result["confidence"] == 50
        assert "invalid JSON" in result["answer"].lower()

    @patch("common.chat_json")
    def test_generate_answer_handles_api_error(self, mock_chat_json: MagicMock) -> None:
        """Test graceful handling of API errors."""
        mock_chat_json.side_effect = RuntimeError("API connection failed")
        
        result = generate_answer("Explain ML")
        
        assert result["confidence"] == 0
        assert "failed" in result["answer"].lower()


class TestEvaluateAnswer:
    """Test answer evaluation with mocked API calls."""

    @patch("evaluator.chat_json")
    def test_evaluate_answer_returns_structure(self, mock_chat_json: MagicMock) -> None:
        """Test that evaluation returns required structure."""
        mock_chat_json.return_value = {
            "score": 85,
            "issues": ["Could be clearer"],
            "improvement_suggestions": ["Add example"]
        }
        
        result = evaluate_answer("Explain ML", "Machine learning is...")
        
        assert "score" in result
        assert "issues" in result
        assert "improvement_suggestions" in result
        assert result["score"] == 85

    @patch("evaluator.chat_json")
    def test_evaluate_answer_validates_score_range(self, mock_chat_json: MagicMock) -> None:
        """Test that scores are in valid 0-100 range."""
        mock_chat_json.return_value = {
            "score": 75,
            "issues": [],
            "improvement_suggestions": []
        }
        
        result = evaluate_answer("Query", "Answer")
        
        assert 0 <= result["score"] <= 100

    @patch("evaluator.chat_json")
    def test_evaluate_answer_handles_parsing_error(self, mock_chat_json: MagicMock) -> None:
        """Test graceful handling of JSON parsing errors in evaluation."""
        mock_chat_json.side_effect = json.JSONDecodeError("msg", "doc", 0)
        
        result = evaluate_answer("Query", "Answer")
        
        assert result["score"] == 50
        assert len(result["issues"]) > 0

    @patch("evaluator.chat_json")
    def test_evaluate_answer_handles_api_error(self, mock_chat_json: MagicMock) -> None:
        """Test graceful handling of API errors in evaluation."""
        mock_chat_json.side_effect = Exception("API error")
        
        result = evaluate_answer("Query", "Answer")
        
        assert result["score"] == 0


class TestRefineAnswer:
    """Test answer refinement with mocked API calls."""

    @patch("refiner.chat_json")
    def test_refine_answer_returns_structure(self, mock_chat_json: MagicMock) -> None:
        """Test that refinement returns required structure."""
        mock_chat_json.return_value = {
            "refined_answer": "Improved answer",
            "changes_made": ["Added clarity"]
        }
        
        result = refine_answer("Original", ["issue"], ["suggestion"])
        
        assert "refined_answer" in result
        assert "changes_made" in result
        assert result["refined_answer"] == "Improved answer"

    @patch("refiner.chat_json")
    def test_refine_answer_handles_parsing_error(self, mock_chat_json: MagicMock) -> None:
        """Test that parsing errors fallback to original answer."""
        mock_chat_json.side_effect = json.JSONDecodeError("msg", "doc", 0)
        
        original = "Original answer"
        result = refine_answer(original, ["issue"], ["suggestion"])
        
        assert result["refined_answer"] == original
        assert len(result["changes_made"]) > 0

    @patch("refiner.chat_json")
    def test_refine_answer_handles_api_error(self, mock_chat_json: MagicMock) -> None:
        """Test that API errors fallback to original answer."""
        mock_chat_json.side_effect = Exception("API failed")
        
        original = "Original answer"
        result = refine_answer(original, ["issue"], ["suggestion"])
        
        assert result["refined_answer"] == original


class TestTokenize:
    """Test text tokenization for memory retrieval."""

    def test_tokenize_basic(self) -> None:
        """Test basic tokenization."""
        tokens = tokenize("hello world")
        assert "hello" in tokens
        assert "world" in tokens

    def test_tokenize_filters_stopwords(self) -> None:
        """Test that stopwords are removed."""
        tokens = tokenize("the quick brown fox")
        assert "the" not in tokens  # Stopword
        assert "quick" in tokens
        assert "brown" in tokens

    def test_tokenize_filters_short_words(self) -> None:
        """Test that words < 3 chars are filtered."""
        tokens = tokenize("a aa aaa")
        assert "a" not in tokens
        assert "aa" not in tokens
        assert "aaa" in tokens

    def test_tokenize_handles_case_insensitivity(self) -> None:
        """Test that tokenization is case-insensitive."""
        tokens = tokenize("Machine Learning")
        assert "machine" in tokens or "learning" in tokens


class TestMemoryFunctions:
    """Test memory loading, saving, and retrieval."""

    def test_load_memory_empty_file(self) -> None:
        """Test loading memory when file doesn't exist."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=True) as f:
            memory = load_memory()
            assert isinstance(memory, list)

    def test_find_relevant_memory_with_overlap(self) -> None:
        """Test finding memories with query overlap."""
        with patch("memory.load_memory") as mock_load:
            mock_load.return_value = [
                {"query": "machine learning basics", "issues": ["too short"], "improvement_suggestions": []},
                {"query": "python programming", "issues": [], "improvement_suggestions": []}
            ]
            
            result = find_relevant_memory("explain machine learning")
            
            # Should find the first memory with overlap
            assert len(result) > 0

    def test_format_memory_context_empty(self) -> None:
        """Test formatting empty memory."""
        result = format_memory_context([])
        assert "No past mistakes" in result

    def test_format_memory_context_with_items(self) -> None:
        """Test formatting memory with items."""
        items = [
            {
                "query": "test query",
                "issues": ["issue1"],
                "improvement_suggestions": ["suggestion1"]
            }
        ]
        result = format_memory_context(items)
        
        assert "test query" in result
        assert "issue1" in result
        assert "suggestion1" in result

    def test_save_memory_skips_api_errors(self) -> None:
        """Test that API errors are not saved to memory."""
        with patch("memory.load_memory") as mock_load, \
             patch.object(Path, "write_text") as mock_write:
            
            mock_load.return_value = []
            evaluation = {
                "score": 0,
                "issues": ["Connection error."],
                "improvement_suggestions": []
            }
            
            save_memory("query", evaluation)
            
            # Should not write to file for API errors
            mock_write.assert_not_called()


class TestIntegration:
    """Integration tests for multi-agent workflows."""

    @patch("pipeline.generate_answer")
    @patch("pipeline.evaluate_answer")
    @patch("pipeline.refine_answer")
    @patch("pipeline.build_portfolio_summary")
    def test_pipeline_single_round(self, mock_portfolio, mock_refine, mock_evaluate, mock_generate):
        """Test complete single-round pipeline."""
        sys.path.insert(0, str(Path(__file__).parent.parent / "agents"))
        from pipeline import run_pipeline
        
        mock_generate.return_value = {
            "answer": "Generated answer",
            "reasoning": "...",
            "confidence": 85
        }
        mock_evaluate.return_value = {
            "score": 92,
            "issues": [],
            "improvement_suggestions": []
        }
        mock_refine.return_value = {
            "refined_answer": "Refined answer",
            "changes_made": []
        }
        mock_portfolio.return_value = {
            "resume_bullets": [],
            "linkedin_post": "",
            "beginner_explanation": ""
        }
        
        result = run_pipeline("Test query", max_rounds=1, target_score=90, save_outputs=False)
        
        assert "query" in result
        assert "final_answer" in result
        assert "final_score" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
