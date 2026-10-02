from __future__ import annotations

import os

from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "yagbu-worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)


@celery_app.task(name="yagbu.worker.ping")
def ping() -> str:
    return "pong"


@celery_app.task(name="yagbu.worker.build_job")
def build_job(job_id: str, prompt: str) -> dict:
    return {"job_id": job_id, "prompt": prompt, "status": "queued"}


__all__ = ["celery_app", "ping", "build_job"]
