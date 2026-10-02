# YAGBU SaaS Foundation

This repository now includes Stage 4.1 foundation for a SaaS-ready inference platform built on top of the open-source YAGBU runtime.

## New structure

```text
.
├── apps/
│   └── web/
│       └── README.md
├── database/
│   └── schema.sql
├── services/
│   ├── api/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── db.py
│   │   │   ├── deps.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── core/
│   │   │   │   ├── __init__.py
│   │   │   │   └── security.py
│   │   │   ├── routers/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── health.py
│   │   │   │   └── models.py
│   │   └── requirements.txt
│   └── worker/
│       ├── app.py
│       └── queue.py
├── docker-compose.yml
├── .env.example
├── README.md
└── ...
```

## What is included

- FastAPI app skeleton for the public API service
- basic auth routes for signup / login / me
- PostgreSQL model schema for SaaS entities
- Redis / Celery style worker foundation
- Docker Compose stack for local development
- model and inference tracking tables for the SaaS layer

## Next phase

Stage 4.2 will add:
- actual model registry service
- API key issuance logic
- usage metering and billing events
- async inference worker integration
- dashboard app shell
