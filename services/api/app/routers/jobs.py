from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])


@router.get("/{job_id}")
def get_job(job_id: str) -> dict:
    """
    Get inference job status.
    """
    return {
        "id": job_id,
        "status": "completed",
        "model": "yagbu-8b",
        "created_at": "2026-10-02T06:30:00Z",
        "completed_at": "2026-10-02T06:30:05Z",
        "result": {
            "text": "YAGBU response text",
            "tokens_generated": 64,
        },
    }


@router.get("")
def list_jobs(status: str | None = None, model: str | None = None) -> dict:
    """
    List inference jobs.
    """
    return {
        "jobs": [
            {
                "id": "job-1",
                "status": "completed",
                "model": "yagbu-8b",
                "created_at": "2026-10-02T06:30:00Z",
            },
            {
                "id": "job-2",
                "status": "running",
                "model": "yagbu-35b",
                "created_at": "2026-10-02T06:31:00Z",
            },
        ]
    }


__all__ = ["router"]
