# Contributing Guidelines

Thank you for your interest in contributing to Aerulias AI! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites
- Python 3.9+
- Git
- Basic understanding of multi-agent systems

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/aerulias_ai.git
cd aerulias_ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Run tests to verify setup
pytest tests/ -v
```

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number
```

### 2. Make Changes

- Follow code style guidelines (see below)
- Write tests for new features
- Update documentation
- Add type hints

### 3. Run Quality Checks

```bash
# Format code
black agents/ tests/

# Lint
flake8 agents/ tests/

# Type check
mypy agents/ --ignore-missing-imports

# Run tests
pytest tests/ -v --cov=agents

# Security check
bandit -r agents/
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add new feature" # Use conventional commits
git push origin feature/your-feature-name
```

### 5. Create Pull Request

- Provide clear description
- Reference related issues
- Ensure CI passes
- Request review from maintainers

## Code Style Guidelines

### Python Style

Follow PEP 8 with these enforcements:

- **Formatter**: Black (line length: 100)
- **Linter**: Flake8
- **Type Checker**: mypy

```bash
# Auto-format
black agents/

# Check style
flake8 agents/

# Check types
mypy agents/
```

### Type Hints

All functions must have type hints:

```python
from typing import Dict, List, Optional, Any

def evaluate_answer(query: str, answer: str) -> Dict[str, Any]:
    """Evaluate an answer.
    
    Args:
        query: User query string
        answer: Answer to evaluate
        
    Returns:
        Dictionary with evaluation results
        
    Raises:
        ValidationError: If inputs are invalid
    """
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def process_query(query: str, max_length: int = 2000) -> str:
    """Process and validate a query string.
    
    This function sanitizes input and ensures it meets length
    requirements for the pipeline.
    
    Args:
        query: Raw query string from user
        max_length: Maximum allowed query length in characters
        
    Returns:
        Processed and validated query string
        
    Raises:
        QueryValidationError: If query is invalid or too long
        
    Example:
        >>> processed = process_query("What is AI?")
        >>> print(processed)
        "what is ai?"
    """
    pass
```

## Testing

### Test Requirements

- Write tests for all new features
- Maintain >80% code coverage
- Include unit and integration tests
- Test error cases

### Test Structure

```python
import pytest
from agents.evaluator import evaluate_answer
from agents.errors import ValidationError

class TestEvaluator:
    """Test suite for evaluator module."""
    
    def test_evaluate_answer_success(self):
        """Test successful evaluation."""
        result = evaluate_answer("What is AI?", "AI is...")
        assert result['score'] >= 0
        assert result['score'] <= 100
    
    def test_evaluate_answer_invalid_query(self):
        """Test evaluation with invalid query."""
        with pytest.raises(ValidationError):
            evaluate_answer("", "Answer")
    
    @pytest.mark.slow
    def test_evaluate_answer_integration(self):
        """Integration test with API."""
        pass
```

### Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=agents --cov-report=html

# Specific test file
pytest tests/test_evaluator.py -v

# Specific test
pytest tests/test_evaluator.py::TestEvaluator::test_evaluate_answer_success -v

# Only fast tests
pytest tests/ -v -m "not slow"
```

## Documentation

### Update Documentation For:
- New APIs
- New features
- Configuration changes
- Architecture changes

### Documentation Locations
- **API Changes**: Update [docs/API.md](docs/API.md)
- **Architecture**: Update [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Deployment**: Update [docs/PRODUCTION_DEPLOYMENT.md](docs/PRODUCTION_DEPLOYMENT.md)
- **General**: Update [README.md](README.md)

## Commit Message Guidelines

Follow Conventional Commits:

```
<type>: <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Test changes
- `chore`: Build, dependencies

### Examples

```bash
git commit -m "feat: add redis caching support"
git commit -m "fix: handle API timeout gracefully"
git commit -m "docs: update deployment guide"
git commit -m "refactor: simplify error handling"
```

## Pull Request Process

1. **Create PR**
   - Title: Clear and descriptive
   - Description: Explain what and why
   - Reference issues: Use `Closes #123`

2. **Example PR Description**
   ```
   ## Description
   Adds Redis caching support to reduce API calls by 40%.
   
   ## Motivation
   High volume users experience latency. Caching will improve response times.
   
   ## Changes
   - Add redis dependency
   - Implement cache layer in common.py
   - Add configuration options
   - Add tests for cache hit/miss
   
   ## Testing
   - All tests pass (pytest -v)
   - Coverage maintained >80%
   - Manual testing: 20 requests, 15 cached
   
   Closes #45
   ```

3. **Review Process**
   - Address feedback constructively
   - Re-request review after changes
   - Don't force push after review started

4. **Merge**
   - Squash commits if requested
   - Delete branch after merge

## Common Issues

### Issue: Tests Failing in CI

```bash
# Run same checks locally
black --check agents/
flake8 agents/
mypy agents/ --ignore-missing-imports
pytest tests/ --cov=agents
```

### Issue: Type Checking Errors

```bash
# Update type hints
mypy agents/ --show-error-codes --strict

# Use Optional for nullable types
from typing import Optional
def function(value: Optional[str] = None) -> None:
    pass
```

### Issue: Test Coverage Low

```bash
# Generate coverage report
pytest tests/ --cov=agents --cov-report=html
# View: htmlcov/index.html
```

## Release Process

### Version Numbering
- Format: `MAJOR.MINOR.PATCH`
- Example: `1.0.0`, `1.2.3`
- Follow Semantic Versioning

### Release Steps

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create tag: `git tag v1.0.0`
4. Push: `git push origin v1.0.0`
5. Create GitHub Release with notes

## Performance Optimization

When optimizing code:

1. **Profile First**: Use cProfile
   ```bash
   python -m cProfile -s cumtime agents/main.py
   ```

2. **Benchmark**: Compare before/after
   ```python
   import timeit
   setup = "from agents.evaluator import evaluate_answer"
   stmt = 'evaluate_answer("What is AI?", "AI is...")'
   timeit.timeit(stmt, setup, number=10)
   ```

3. **Document**: Add comments about optimizations

## Security

### Security Issues

⚠️ **Do not** open public issues for security vulnerabilities.

Instead, email: security@aerulias.ai

### Security Practices

- Use environment variables for secrets
- Validate all inputs
- Sanitize error messages
- Keep dependencies updated
- Run security scans: `bandit -r agents/`

## Questions?

- 📖 Check [docs/](docs/)
- 💬 Open Discussion on GitHub
- 📧 Email: maintainers@aerulias.ai

---

Thank you for contributing! ❤️
