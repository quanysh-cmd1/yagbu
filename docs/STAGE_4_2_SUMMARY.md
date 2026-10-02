# YAGBU Stage 4.2: Model Registry and Deployment

This phase extends the SaaS foundation with a functional model registry, deployment management, and async inference orchestration.

## New features in Stage 4.2

### 1. Model Registry
- `/v1/models` — list available models
- `/v1/models/{model_id}` — get model details
- `/v1/models/{model_id}/register-adapter` — register LoRA/prerouter/recover adapters

### 2. Deployment Management
- `/v1/deployments` — create and list deployments
- `/v1/deployments/{deployment_id}` — get status
- `/v1/deployments/{deployment_id}/status` — update status (start/stop/scale)
- `/v1/deployments/{deployment_id}/metrics` — get health and performance metrics

### 3. Inference API (OpenAI-compatible)
- `/v1/chat/completions` — synchronous chat completions
- `/v1/chat/completions/async` — asynchronous job submission
- `/v1/jobs/{job_id}` — poll job status
- `/v1/jobs` — list jobs

### 4. Job Orchestration
- Redis-backed job queue (`JobQueue`)
- Celery workers for async processing
- Job status tracking: queued → running → completed/failed
- Result storage with expiration

### 5. Database models
- `Adapter` — adapter (LoRA, prerouter, recover) metadata
- `Deployment` — model deployment with region, replicas, memory budget
- `DeploymentMetrics` — performance tracking

## API endpoints summary

```
GET    /health
POST   /auth/signup
POST   /auth/login
GET    /auth/me

GET    /v1/models
GET    /v1/models/{model_id}
POST   /v1/models/{model_id}/register-adapter

POST   /v1/deployments
GET    /v1/deployments/{deployment_id}
PUT    /v1/deployments/{deployment_id}/status
GET    /v1/deployments/{deployment_id}/metrics

POST   /v1/chat/completions
POST   /v1/chat/completions/async
GET    /v1/jobs/{job_id}
GET    /v1/jobs
```

## Run locally

```bash
cd services/api
pip install -r requirements.txt

cd ..
cp .env.example .env
docker compose up --build

# Then test
curl http://localhost:8000/health
curl -X POST http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"yagbu-8b","messages":[{"role":"user","content":"Hello"}]}'
```

## Next steps (Stage 4.3)

- Real model loading and inference backend
- Streaming inference responses
- Better error handling and validation
- Request authentication with API keys
- Usage metering and billing integration
