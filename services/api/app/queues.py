from __future__ import annotations

from pathlib import Path

from redis import Redis


class JobQueue:
    """Redis-backed job queue for async inference tasks."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.client = Redis.from_url(redis_url, decode_responses=True)
        self.queue_key = "yagbu:queue:jobs"
        self.result_key_prefix = "yagbu:result:"

    def enqueue(self, job_id: str, deployment_id: str, job_type: str, payload: dict) -> dict:
        item = {
            "id": job_id,
            "deployment_id": deployment_id,
            "job_type": job_type,
            "payload": payload,
            "status": "queued",
        }
        self.client.rpush(self.queue_key, str(item))
        return item

    def dequeue(self) -> dict | None:
        item = self.client.lpop(self.queue_key)
        if item is None:
            return None
        import ast

        return ast.literal_eval(item)

    def set_result(self, job_id: str, result: dict) -> None:
        self.client.set(f"{self.result_key_prefix}{job_id}", str(result), ex=86400)

    def get_result(self, job_id: str) -> dict | None:
        item = self.client.get(f"{self.result_key_prefix}{job_id}")
        if item is None:
            return None
        import ast

        return ast.literal_eval(item)

    def queue_size(self) -> int:
        return int(self.client.llen(self.queue_key))


__all__ = ["JobQueue"]
