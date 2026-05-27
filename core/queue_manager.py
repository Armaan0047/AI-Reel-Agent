"""AI Reel Agent v5.0 — Render Queue Manager"""
import uuid
import time


class RenderQueue:
    """In-memory render job queue."""

    def __init__(self):
        self._queue = []

    def add(self, job_config: dict) -> str:
        """Add a job to the queue. Returns job ID."""
        job_id = str(uuid.uuid4())[:8]
        job = {
            "id": job_id,
            "config": job_config,
            "status": "queued",
            "created": time.time(),
            "output": None,
            "error": None,
        }
        self._queue.append(job)
        return job_id

    def remove(self, job_id: str) -> bool:
        """Remove a job from the queue."""
        for i, job in enumerate(self._queue):
            if job["id"] == job_id:
                self._queue.pop(i)
                return True
        return False

    def list_jobs(self) -> list:
        """Return all jobs in the queue."""
        return self._queue.copy()

    def get_next(self) -> dict | None:
        """Get the next queued job without removing it."""
        for job in self._queue:
            if job["status"] == "queued":
                return job
        return None

    def mark_processing(self, job_id: str):
        for job in self._queue:
            if job["id"] == job_id:
                job["status"] = "processing"

    def mark_complete(self, job_id: str, output_path: str):
        for job in self._queue:
            if job["id"] == job_id:
                job["status"] = "complete"
                job["output"] = output_path

    def mark_failed(self, job_id: str, error: str):
        for job in self._queue:
            if job["id"] == job_id:
                job["status"] = "failed"
                job["error"] = error

    def clear(self):
        self._queue.clear()

    def get_status(self) -> dict:
        """Get queue statistics."""
        statuses = {"queued": 0, "processing": 0, "complete": 0, "failed": 0}
        for job in self._queue:
            statuses[job["status"]] = statuses.get(job["status"], 0) + 1
        return {
            "total": len(self._queue),
            **statuses,
        }

    def get_completed(self) -> list:
        return [j for j in self._queue if j["status"] == "complete"]
