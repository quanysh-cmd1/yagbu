# Stage 4.1 Foundation for YAGBU SaaS

This phase creates a simple SaaS foundation around the YAGBU runtime so the platform can evolve into a production inference service.

## Included

- FastAPI app for public API
- auth endpoints and JWT-aware dependency placeholders
- PostgreSQL schema for users, orgs, models, jobs, usage
- Redis / worker queue foundation
- Docker Compose local stack
- dashboard app placeholder

## Run locally

```bash
cp .env.example .env

docker compose up --build

# Then the API will be available at
# http://localhost:8000/
# and health at
# http://localhost:8000/health
```

## Stage 4.1 goals

- foundational SaaS backend
- user and organization model
- API and model registry shell
- queue and local worker background pattern
- ready to extend with auth, billing, telemetry, and deployments
