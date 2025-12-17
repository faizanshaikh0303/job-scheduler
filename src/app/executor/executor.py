
from app.jobs.registry import get_job
from app.jobs.models import Job, JobStatus


class JobExecutor:
    def execute(self, job: Job):
        job.status = JobStatus.RUNNING
        try:
            fn = get_job(job.name)
            fn(job.payload)
            job.status = JobStatus.SUCCESS
        except Exception as e:
            job.retries += 1
            if job.retries >= job.max_retries:
                job.status = JobStatus.FAILED
            else:
                job.status = JobStatus.PENDING
            print(f"[ERROR] Job {job.id}: {e}")
