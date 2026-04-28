# Production Deployment Guide

## Pre-Deployment Checklist

- [ ] All tests passing (`pytest tests/`)
- [ ] Code quality checks passed (`black`, `mypy`, `flake8`)
- [ ] Security scan completed (`bandit`, `safety`)
- [ ] Environment variables configured
- [ ] API keys rotated
- [ ] Database migrations completed
- [ ] Monitoring/logging configured
- [ ] Load testing completed
- [ ] Disaster recovery plan documented
- [ ] Team trained on deployment process

---

## Environment Setup

### 1. Production Environment Variables

Create `.env.production`:

```env
ENV=production
DEBUG=false
OPENROUTER_API_KEY=your_prod_api_key
OPENROUTER_MODEL=openai/gpt-4-turbo
LOG_LEVEL=INFO
LOG_FORMAT=json

# Performance tuning
WORKERS=8
EVALUATOR_TARGET_SCORE=85
REFINER_MAX_ITERATIONS=5
MEMORY_ENABLED=true

# Rate limiting
RATE_LIMIT_PER_MINUTE=120

# Caching
CACHE_TTL_SECONDS=3600
```

### 2. Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install production dependencies
pip install -r requirements.txt
pip install gunicorn[gevent]  # Production WSGI server
```

---

## Docker Deployment

### 1. Build Docker Image

```bash
docker build -t aerulias_ai:latest .
docker tag aerulias_ai:latest aerulias_ai:v1.0.0
```

### 2. Run Docker Container

```bash
docker run -d \
  --name aerulias_api \
  -p 8000:8000 \
  --env-file .env.production \
  --restart unless-stopped \
  --memory 2g \
  --cpus 2 \
  aerulias_ai:latest
```

### 3. Docker Compose (Multi-service)

See `docker-compose.yml` for production setup with:
- API server
- Redis cache
- PostgreSQL (optional)
- Prometheus monitoring

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Gunicorn Deployment (Linux/Mac)

### 1. Configuration File (`gunicorn.conf.py`)

```python
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'aerulias_api'

# Server hooks
def on_starting(server):
    print("Gunicorn server is starting...")

def when_ready(server):
    print("Gunicorn server is ready. Spawning workers")
```

### 2. Systemd Service File (`/etc/systemd/system/aerulias.service`)

```ini
[Unit]
Description=Aerulias AI API
After=network.target

[Service]
User=aerulias
WorkingDirectory=/home/aerulias/aerulias_ai
ExecStart=/home/aerulias/aerulias_ai/venv/bin/gunicorn \
    -c gunicorn.conf.py \
    api_server:app
Restart=always
RestartSec=10

# Resource limits
MemoryLimit=2G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
```

### 3. Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl start aerulias
sudo systemctl enable aerulias
```

---

## Cloud Platform Deployments

### Railway/Render/Heroku

1. **Configure Procfile** (already included):
```
web: gunicorn api_server:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **Set Environment Variables** in platform dashboard

3. **Deploy**:
```bash
# Railway
railway up

# Render
render deploy

# Heroku
git push heroku main
```

### Azure App Service

```bash
# Create resource group
az group create --name aerulias-rg --location eastus

# Create App Service Plan
az appservice plan create \
  --name aerulias-plan \
  --resource-group aerulias-rg \
  --sku B2 \
  --is-linux

# Create web app
az webapp create \
  --resource-group aerulias-rg \
  --plan aerulias-plan \
  --name aerulias-api \
  --runtime "PYTHON:3.10"

# Deploy code
az webapp deployment source config-zip \
  --resource-group aerulias-rg \
  --name aerulias-api \
  --src deploy.zip
```

### AWS Lambda (Serverless)

Use AWS SAM or Serverless Framework:

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    MemorySize: 512

Resources:
  AeruliasFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      Handler: api_server.handler
      Runtime: python3.10
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /{proxy+}
            Method: ANY
```

---

## Monitoring & Logging

### 1. Logging Setup

All logs automatically output to stdout in JSON format for cloud platforms:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "logger": "agents.pipeline",
  "message": "Pipeline execution complete",
  "duration_ms": 3420,
  "score": 87
}
```

### 2. Structured Logging in Application

```python
import logging
logger = logging.getLogger(__name__)

# Automatic JSON formatting when LOG_FORMAT=json
logger.info("User query processed", extra={
    "query_length": len(query),
    "score": score,
    "iterations": iterations
})
```

### 3. Health Checks

The API provides health endpoint for load balancers:

```bash
# Health check endpoint
GET /api/v1/health

# Expected response (200 OK)
{
  "status": "healthy",
  "components": {
    "api": "ok",
    "llm_client": "ok"
  }
}
```

### 4. Prometheus Metrics (Planned v2.0)

```bash
GET /metrics

# Metrics include:
# - request_count_total
# - request_duration_seconds
# - answer_score
# - llm_api_duration_seconds
```

---

## Scaling Strategies

### Horizontal Scaling

1. **Load Balancer Setup** (nginx example):
```nginx
upstream aerulias_backend {
    server api1.example.com:8000;
    server api2.example.com:8000;
    server api3.example.com:8000;
}

server {
    listen 80;
    server_name api.aerulias.ai;
    
    location / {
        proxy_pass http://aerulias_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

2. **Container Orchestration** (Kubernetes):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aerulias-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aerulias-api
  template:
    metadata:
      labels:
        app: aerulias-api
    spec:
      containers:
      - name: api
        image: aerulias_ai:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Caching Strategy

- Use Redis for session/query caching
- Implement CDN for static assets
- Client-side caching with ETags

---

## Disaster Recovery

### Backup Strategy

```bash
# Daily backup to S3
0 2 * * * /scripts/backup_to_s3.sh

# Weekly backup to local storage
0 3 * * 0 /scripts/backup_local.sh
```

### Recovery Procedures

1. **Database Restore**
```bash
# Restore from S3
aws s3 cp s3://aerulias-backups/db-backup.sql ./backup.sql
psql -d aerulias_db -f backup.sql
```

2. **Configuration Restore**
```bash
# Restore from git
git checkout <commit-hash> -- .env
```

---

## Security Best Practices

✅ **Implemented**
- Environment-based configuration
- API key rotation support
- Input validation
- Error message sanitization
- Rate limiting

🔐 **Recommendations**
- Use HTTPS/TLS only
- Implement WAF (Web Application Firewall)
- Enable CORS selectively
- Rotate API keys monthly
- Monitor for suspicious patterns
- Run security scans regularly

---

## Performance Tuning

### Database Optimization
- Connection pooling (min: 5, max: 20)
- Query optimization
- Indexing strategy
- Caching layer

### API Optimization
- Response compression (gzip)
- Connection keep-alive
- Request batching
- Async processing

### Model Selection
- Use faster model for generation (gpt-4o-mini)
- Use precise model for evaluation
- Batch API requests where possible

---

## Troubleshooting

### High Latency
1. Check worker pool size
2. Monitor LLM API response times
3. Review query complexity
4. Check memory usage

### High Error Rate
1. Check API key validity
2. Review rate limiting
3. Monitor token usage
4. Check network connectivity

### Memory Leaks
1. Monitor process memory growth
2. Check for circular dependencies
3. Review memory caching strategy
4. Profile with memory_profiler

---

## Rollback Procedure

```bash
# If deployment fails, rollback to previous version
docker pull aerulias_ai:v0.9.9
docker stop aerulias_api
docker run -d --name aerulias_api aerulias_ai:v0.9.9

# Or with git
git revert <commit-hash>
git push heroku main
```

---

## Support & Maintenance

- **Monitoring Dashboard**: Datadog, New Relic, or custom
- **Error Tracking**: Sentry integration (planned v2.0)
- **Performance Profiling**: Enable with PROFILE=1
- **Logs Aggregation**: ELK stack or cloud provider solution

For additional help, see `ROADMAP.md` and GitHub Issues.
