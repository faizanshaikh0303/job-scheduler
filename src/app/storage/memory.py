
from typing import Dict, List
from app.jobs.models import Job


class InMemoryJobStore:
    def __init__(self):
        self.jobs: Dict[str, Job] = {}

    def add(self, job: Job):
        self.jobs[job.id] = job

    def get_due_jobs(self, now):
        return [
            job for job in self.jobs.values()
            if job.run_at <= now and job.status == "pending"
        ]

    def update(self, job: Job):
        self.jobs[job.id] = job
    
    def get(self, job_id: str):
        return self.jobs.get(job_id)

