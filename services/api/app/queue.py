from __future__ import annotations

import json
from typing import Any

import redis

from .core.config import settings


class JobQueue:
    """Redis-backed job queue for async inference tasks."""

    def __init__(self, redis_url: str = settings.redis_url):
        self.redis_url = redis_url
        self.client = redis.from_url(redis_url)
        self.queue_key = "yagbu:queue:jobs"
        self.result_key_prefix = "yagbu:result:"

    def enqueue(
        self,
        job_id: str,
        deployment_id: str,
        job_type: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Enqueue a new inference job.
        """
        job = {
            "id": job_id,
            "deployment_id": deployment_id,
            "job_type": job_type,
            "payload": payload,
            "status": "queued",
        }
        self.client.rpush(self.queue_key, json.dumps(job))
        return job

    def dequeue(self) -> dict[str, Any] | None:
        """
        Dequeue a job for processing.
        """
        data = self.client.lpop(self.queue_key)
        if data:
            return json.loads(data)
        return None

    def set_result(self, job_id: str, result: dict[str, Any]) -> None:
        """
        Store the result of a completed job.
        """
        key = f"{self.result_key_prefix}{job_id}"
        self.client.set(key, json.dumps(result), ex=86400)  # Expire in 24h

    def get_result(self, job_id: str) -> dict[str, Any] | None:
        """
        Retrieve the result of a job.
        """
        key = f"{self.result_key_prefix}{job_id}"
        data = self.client.get(key)
        if data:
            return json.loads(data)
        return None

    def get_queue_size(self) -> int:
        """
        Get current queue depth.
        """
        return self.client.llen(self.queue_key)


__all__ = ["JobQueue"]
