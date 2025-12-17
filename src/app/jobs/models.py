
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
import uuid


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"


class Job(BaseModel):
    id: str
    name: str
    run_at: datetime
    payload: Dict[str, Any]
    status: JobStatus = JobStatus.PENDING
    retries: int = 0
    max_retries: int = 3

    @staticmethod
    def create(name: str, run_at: datetime, payload: Dict[str, Any]):
        return Job(
            id=str(uuid.uuid4()),
            name=name,
            run_at=run_at,
            payload=payload,
        )
