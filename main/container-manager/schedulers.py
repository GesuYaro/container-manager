import time

import schedule
import threading

from jobs import CheckpointJob
from jobs import RestoreJob
from jobs import DeleteUnusedCheckpointsJob
from checkpointers import CheckpointService
from clients import ClientPool


def jobs_loop():
    schedule.run_pending()
    time.sleep(1)


def schedule_jobs(client_pool: ClientPool):
    checkpoint_service = CheckpointService()

    checkpoint_job = CheckpointJob(
        client_pool=client_pool,
        checkpoint_service=checkpoint_service
    )

    restore_job = RestoreJob(
        client_pool=client_pool,
        checkpoint_service=checkpoint_service
    )

    delete_job = DeleteUnusedCheckpointsJob(
        client_pool=client_pool,
        checkpoint_service=checkpoint_service
    )

    schedule.every(1).minute.do(checkpoint_job.run)
    schedule.every(1).minute.do(restore_job.run)
    schedule.every(1).minute.do(delete_job.run)
    jobs_thread = threading.Thread(target=jobs_loop)
    jobs_thread.start()





