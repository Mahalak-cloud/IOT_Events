import time
import threading
from rq import Worker, Queue

from rq.job import Job


class WindowsWorker(Worker):
    def __init__(self, queues, *args, timeout=30, **kwargs):
        super().__init__(queues, *args, **kwargs)
        self.timeout = timeout  # Set timeout as an instance variable

    def perform_job(self, job):
        """Perform the job with a timeout."""
        timeout_event = threading.Event()

        def job_target():
            try:
                job.perform()
            finally:
                timeout_event.set()  # Signal that job is done

        job_thread = threading.Thread(target=job_target)
        job_thread.start()

        if not timeout_event.wait(timeout=self.timeout):
            # Job timed out
            print(f"Job {job.id} timed out")
            job.meta['status'] = 'timeout'
            job.save_meta()
            job.fail('Job timed out')
            job_thread.join()  # Ensure the job thread has finished

    def work(self, *args, **kwargs):
        """Override the work method to handle job processing."""
        while True:
            super().work(*args, **kwargs)  # Call the base method to process jobs
