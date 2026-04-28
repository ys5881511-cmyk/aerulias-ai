# Aerulias AI - Engineering Best Practices & Architecture

## Overview

Aerulias AI demonstrates enterprise-grade software engineering practices across multiple domains:
- **System Design**: Multi-agent orchestration with feedback loops
- **Code Quality**: Type hints, comprehensive docstrings, structured logging
- **Testing**: Unit tests with mocking, 80%+ code coverage
- **DevOps**: Docker containerization, GitHub Actions CI/CD
- **Production Readiness**: Error handling, graceful degradation, monitoring

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Dashboard (Web UI)                       │
│              HTML + CSS + JavaScript + Chart.js              │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Dashboard Server (HTTP)                     │
│          python dashboard_server.py --port 8000              │
└────────────────────────┬────────────────────────────────────┘
                         │ Orchestrates
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Pipeline Orchestrator                        │
│  • Coordinates multi-round generate-evaluate-refine loops   │
│  • Manages memory and source context                        │
│  • Builds portfolio summaries                               │
└──────┬──────────┬──────────┬──────────┬────────────────────┘
       │          │          │          │
       ▼          ▼          ▼          ▼
┌─────────────┬──────────┬──────────┬──────────┐
│ Generator   │Evaluator │ Refiner  │Portfolio │
│  Agent      │ Agent    │ Agent    │Generator │
└─────────────┴──────────┴──────────┴──────────┘
       │          │          │          │
       └──────────┴──────────┴──────────┘
              │ Uses
              ▼
    ┌──────────────────┐
    │ OpenRouter API   │
    │ (LLM Backend)    │
    └──────────────────┘
```

### Data Flow

1. **User Query** → Dashboard UI
2. **HTTP Request** → Dashboard Server
3. **Pipeline Execution**:
   - Load relevant memory
   - Load source documents
   - Generate initial answer
   - Evaluate answer (0-100 score)
   - If score < target: Refine answer (repeat)
   - Save results to history and memory

4. **Response** → Dashboard displays results

---

## Code Quality Standards

### 1. Type Hints (PEP 484)

**Why**: Enables IDE autocompletion, catches errors before runtime, improves code clarity

```python
from typing import Dict, List, Any, Optional

def process_query(query: str, context: Optional[str] = None) -> Dict[str, Any]:
    """Process a query with optional context."""
    pass
```

### 2. Docstrings (Google Style)

**Why**: Enables automatic documentation generation, clarifies intent

```python
def evaluate_answer(query: str, answer: str) -> Dict[str, Any]:
    """Evaluate an answer for quality and hallucination risk.
    
    Args:
        query: Original user query.
        answer: Answer text to evaluate.
        
    Returns:
        Dictionary with 'score', 'issues', 'improvement_suggestions'.
        
    Raises:
        ValueError: If answer evaluation fails.
    """
```

### 3. Structured Logging

**Why**: Enables production monitoring, debugging, and alerting

```python
import logging

logger = logging.getLogger(__name__)

# Instead of print():
logger.info(f"Processing query: {query[:50]}...")
logger.warning(f"Retrying API call: {retry_count}")
logger.error(f"Failed: {error}", exc_info=True)
```

### 4. Error Handling

**Why**: Prevents cascading failures, provides graceful degradation

```python
try:
    result = chat_json(prompt)
except json.JSONDecodeError as e:
    logger.error(f"JSON parsing failed: {e}")
    return fallback_result()
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise
```

---

## Testing Strategy

### Test Organization

```
tests/
├── test_agents.py          # Unit tests for all agents
├── test_integration.py     # End-to-end pipeline tests
└── conftest.py            # Pytest fixtures and configuration
```

### Test Coverage

- **Unit Tests**: Test individual functions with mocked dependencies
- **Integration Tests**: Test multi-agent workflows
- **Mocking**: Mock API calls to ensure fast, deterministic tests
- **Target**: 80%+ code coverage

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=agents --cov-report=html

# Run specific test class
pytest tests/test_agents.py::TestGenerateAnswer -v

# Run with markers
pytest -m unit  # Only unit tests
```

---

## DevOps & Deployment

### Docker Containerization

**Benefits**:
- Consistent environments across machines
- Easy deployment to cloud platforms
- Isolation from system dependencies
- Production-grade health checks

```bash
# Build image
docker build -t aerulias-ai .

# Run container
docker run -p 8000:8000 -e OPENROUTER_API_KEY=... aerulias-ai

# Or use docker-compose
docker-compose up
```

### GitHub Actions CI/CD

**Pipeline**:
1. **Lint** (flake8) - Code style
2. **Type Check** (mypy) - Type annotations
3. **Format Check** (black) - Code formatting
4. **Unit Tests** - Pytest with coverage
5. **Security Scan** (bandit) - Vulnerability detection
6. **Build** - Package creation
7. **Upload** - Artifacts and coverage reports

**Features**:
- Runs on every push and pull request
- Tests on Python 3.10, 3.11, 3.12
- Uploads coverage to Codecov
- Fails on critical security issues

---

## Production Considerations

### 1. Configuration Management

```python
# .env file (not in git)
OPENROUTER_API_KEY=sk_...
OPENROUTER_MODEL=openai/gpt-4o-mini
LOG_LEVEL=INFO
```

### 2. Logging Strategy

```
INFO: Pipeline started
INFO: Round 1 complete. Score: 78
INFO: Target reached. Stopping.
INFO: Pipeline complete. Final score: 92
ERROR: API connection failed (with full traceback)
```

### 3. Error Recovery

- **API Errors**: Fallback to previous answer + log error
- **JSON Parsing**: Return default response with confidence=50
- **Missing Memory**: Continue without memory context
- **File I/O**: Log warning but continue execution

### 4. Performance Metrics

Collect and log:
- **Latency**: Time per round
- **Quality**: Score progression across rounds
- **Cost**: Token usage (if needed)
- **Reliability**: Error rates per component

---

## Development Workflow

### 1. Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python agents/main.py "Your query here"
```

### 3. Run Dashboard

```bash
python dashboard_server.py
# Open http://localhost:8000
```

### 4. Run Tests

```bash
pytest tests/ -v --cov=agents
```

### 5. Format & Lint

```bash
black agents/
flake8 agents/
mypy agents/
```

---

## Best Practices Checklist

✅ **Code Quality**
- [x] Type hints on all functions
- [x] Comprehensive docstrings
- [x] Structured logging throughout
- [x] Consistent error handling

✅ **Testing**
- [x] Unit tests with mocks
- [x] Integration tests
- [x] Coverage reports (80%+)
- [x] Pytest configuration

✅ **DevOps**
- [x] Dockerfile with health checks
- [x] docker-compose for local dev
- [x] GitHub Actions CI/CD pipeline
- [x] Multi-version Python testing

✅ **Documentation**
- [x] Architecture diagrams
- [x] API documentation
- [x] Deployment guides
- [x] Contributing guidelines

✅ **Production Ready**
- [x] Graceful error handling
- [x] Configuration management
- [x] Monitoring & logging
- [x] Security scanning

---

## Interview Talking Points

1. **Why type hints?** "Catches errors early, enables IDE autocompletion, documents function signatures"

2. **Why comprehensive logging?** "Essential for production debugging and monitoring. Better than print() for understanding system behavior"

3. **Why mocked unit tests?** "Fast, deterministic, and don't depend on external APIs. CI/CD can run them instantly"

4. **Why Docker?** "Ensures consistency across environments. Simplifies deployment to any cloud platform"

5. **Why CI/CD?** "Automates quality checks on every commit. Catches regressions early"

---

## Next Steps for Production

1. **Database**: Replace JSON with PostgreSQL for scalability
2. **Authentication**: Add API keys and user management
3. **Rate Limiting**: Protect against abuse
4. **Monitoring**: Add Prometheus metrics and alerts
5. **Caching**: Add Redis for frequently-used results
6. **Async**: Make API calls concurrent for faster processing
