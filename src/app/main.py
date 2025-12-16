from fastapi import FastAPI
from datetime import datetime, timedelta, timezone
from contextlib import asynccontextmanager
import threading

from app.jobs.models import Job
from app.storage.memory import InMemoryJobStore
from app.scheduler.scheduler import Scheduler
import app.jobs.registry


store = InMemoryJobStore()
scheduler = Scheduler(store)


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(target=scheduler.start, daemon=True)
    thread.start()
    print("[APP] Scheduler running")
    yield
    print("[APP] App shutdown")


app = FastAPI(lifespan=lifespan)


@app.post("/schedule")
def schedule_job(name: str, delay_seconds: int, payload: dict):
    run_at = datetime.now(timezone.utc) + timedelta(seconds=delay_seconds)
    job = Job.create(name, run_at, payload)
    store.add(job)
    return {"job_id": job.id, "status": job.status}

from fastapi import HTTPException

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = store.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs")
def list_jobs():
    return list(store.jobs.values())


@app.get("/")
def root():
    return {
        "service": "job-scheduler",
        "status": "ok",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health")
def health():
    return {"ok": True}
