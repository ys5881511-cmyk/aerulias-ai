# API Documentation - Aerulias AI

## Base URL

```
http://localhost:8000
```

## Authentication

All API requests require the following header:
```
Authorization: Bearer YOUR_API_KEY
```

(For development, this can be disabled via environment variable)

## Endpoints

### 1. Improve Answer

**POST** `/api/v1/improve`

Submits a query-answer pair for evaluation and refinement.

#### Request Body

```json
{
  "query": "What is machine learning?",
  "answer": "Machine learning is a field of AI that enables systems to learn...",
  "target_score": 80,
  "max_iterations": 3
}
```

#### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | ✅ | User query (5-2000 chars) |
| answer | string | ✅ | Answer to improve (10-8000 chars) |
| target_score | integer | ❌ | Target evaluation score (0-100, default: 80) |
| max_iterations | integer | ❌ | Max refinement iterations (1-10, default: 3) |
| use_memory | boolean | ❌ | Use memory store (default: true) |

#### Response

```json
{
  "success": true,
  "data": {
    "query": "What is machine learning?",
    "original_answer": "Machine learning is a field...",
    "final_answer": "Machine learning is a sophisticated field of AI...",
    "score": 87,
    "original_score": 72,
    "score_improvement": 15,
    "iterations": 2,
    "refinement_history": [
      {
        "iteration": 1,
        "score": 78,
        "issues": ["Missing examples", "Could be more detailed"],
        "improvements": ["Added use case examples", "Expanded explanation"]
      }
    ],
    "execution_time_ms": 3420,
    "hallucination_risk": "low",
    "cached": false
  }
}
```

#### Status Codes

- **200 OK**: Successful improvement
- **400 Bad Request**: Invalid input
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server error

#### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/improve \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How do neural networks work?",
    "answer": "Neural networks are inspired by biology.",
    "target_score": 85
  }'
```

---

### 2. Evaluate Answer

**POST** `/api/v1/evaluate`

Evaluates a single answer without refinement.

#### Request Body

```json
{
  "query": "What is machine learning?",
  "answer": "Machine learning is a field of AI..."
}
```

#### Response

```json
{
  "success": true,
  "data": {
    "score": 72,
    "issues": [
      "Missing specific examples",
      "Could explain practical applications"
    ],
    "improvement_suggestions": [
      "Add 2-3 real-world use cases",
      "Explain how it differs from traditional programming",
      "Mention common algorithms"
    ]
  }
}
```

---

### 3. Generate Answer

**POST** `/api/v1/generate`

Generates an answer for a query without evaluation or refinement.

#### Request Body

```json
{
  "query": "Explain quantum computing"
}
```

#### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | ✅ | User query (5-2000 chars) |
| context | string | ❌ | Additional context |

#### Response

```json
{
  "success": true,
  "data": {
    "query": "Explain quantum computing",
    "answer": "Quantum computing is a revolutionary approach...",
    "execution_time_ms": 1200
  }
}
```

---

### 4. Health Check

**GET** `/api/v1/health`

Check API health status.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "components": {
    "api": "ok",
    "llm_client": "ok",
    "memory_store": "ok"
  }
}
```

---

### 5. Get Metrics

**GET** `/api/v1/metrics`

Get system metrics and statistics.

#### Response

```json
{
  "success": true,
  "data": {
    "total_requests": 1523,
    "avg_execution_time_ms": 2840,
    "avg_score_before": 68,
    "avg_score_after": 84,
    "avg_improvement": 16,
    "cache_hit_rate": 0.42,
    "error_rate": 0.02,
    "uptime_hours": 72.5
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_QUERY",
    "message": "Query must be between 5-2000 characters",
    "severity": "warning",
    "details": {
      "field": "query",
      "received_length": 3
    }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_QUERY | 400 | Query validation failed |
| INVALID_ANSWER | 400 | Answer validation failed |
| INVALID_INPUT | 400 | General input validation error |
| API_FAILURE | 500 | LLM API failure |
| API_TIMEOUT | 504 | LLM API timeout |
| RATE_LIMIT_EXCEEDED | 429 | Rate limit exceeded |
| AUTHENTICATION_ERROR | 401 | Invalid API key |
| INTERNAL_ERROR | 500 | Internal server error |

---

## Rate Limiting

- **Default**: 60 requests per minute per API key
- **Response Headers**:
  - `X-RateLimit-Limit`: Total requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Unix timestamp of rate limit reset

```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1705316400
```

---

## Pagination (Batch Endpoints)

Not currently supported, but planned for v2.0.

---

## Versioning

- **Current Version**: v1
- **API Format**: `/api/v1/...`
- **Deprecation Policy**: 12 months notice before removing deprecated endpoints

---

## SDK Examples

### Python

```python
import requests

api_key = "your_api_key"
headers = {"Authorization": f"Bearer {api_key}"}

response = requests.post(
    "http://localhost:8000/api/v1/improve",
    headers=headers,
    json={
        "query": "What is AI?",
        "answer": "AI is intelligence in machines.",
        "target_score": 85
    }
)

result = response.json()
print(f"Final Score: {result['data']['score']}")
print(f"Final Answer: {result['data']['final_answer']}")
```

### JavaScript/Node.js

```javascript
const response = await fetch('http://localhost:8000/api/v1/improve', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'What is AI?',
    answer: 'AI is intelligence in machines.',
    target_score: 85
  })
});

const result = await response.json();
console.log(`Final Score: ${result.data.score}`);
```

---

## Webhook Support (Planned v2.0)

Support for async processing with webhook callbacks for long-running requests.

---

## Changelog

### v1.0.0
- Initial API release
- Endpoints: improve, evaluate, generate, health, metrics
- Rate limiting support
- Structured error handling

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/yourname/aerulias_ai/issues
- Email: support@aerulias.ai
- Documentation: https://docs.aerulias.ai
