# src/app/scheduler/scheduler.py
import time
from datetime import datetime, timezone
from app.storage.memory import InMemoryJobStore
from app.executor.executor import JobExecutor

class Scheduler:
    def __init__(self, store: InMemoryJobStore):
        self.store = store
        self.executor = JobExecutor()

    def start(self, poll_interval=1):
        print("[SCHEDULER] Started")
        while True:
            now = datetime.now(timezone.utc)  # ✅ aware UTC
            due_jobs = self.store.get_due_jobs(now)

            for job in due_jobs:
                self.executor.execute(job)
                self.store.update(job)

            time.sleep(poll_interval)
