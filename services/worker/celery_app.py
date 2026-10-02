from __future__ import annotations

from celery import Celery

celery_app = Celery(
    "yagbu_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


@celery_app.task(name="yagbu.process_inference")
def process_inference(job_id: str, deployment_id: str, payload: dict) -> dict:
    """
    Dummy worker implementation. Real model calls will replace this later.
    """
    return {
        "id": job_id,
        "deployment_id": deployment_id,
        "status": "completed",
        "response": {
            "text": f"Processed job {job_id} for deployment {deployment_id}",
            "tokens": 128,
        },
    }


@celery_app.task(name="yagbu.check_health")
def check_health(deployment_id: str) -> dict:
    return {"deployment_id": deployment_id, "status": "healthy"}


__all__ = ["celery_app", "process_inference", "check_health"]
