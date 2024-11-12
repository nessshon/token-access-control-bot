from typing import Union

from apscheduler.events import EVENT_JOB_ERROR
from apscheduler.job import Job
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from . import tasks
from .errors import on_job_error
from ..config import Config


class Scheduler:
    """
    A class representing a scheduler for managing and running jobs using AsyncIOScheduler.
    """
    schedulers = {}

    def __init__(self, config: Config) -> None:
        """
        Initialize the Scheduler.

        :param config: The Config object.
        """
        self.config = config
        self.scheduler = self.new(1)

    def new(self, db: int) -> AsyncIOScheduler:
        job_store = RedisJobStore(
            host=self.config.redis.HOST,
            port=self.config.redis.PORT,
            db=self.config.redis.DB + db,
        )
        scheduler = AsyncIOScheduler(
            jobstores={'default': job_store},
        )
        self.schedulers[db] = scheduler
        return scheduler

    def get_all_job_ids(self) -> list[str]:
        """
        Get a list of all job IDs.

        :return: List of job IDs.
        """
        return [job.id for job in self.scheduler.get_jobs()]

    def _delete_job(self, job_id: str) -> Union[Job, None]:
        """
        Delete a job with the given ID.

        :param job_id: The ID of the job to be deleted.
        :return: Deleted Job object or None if the job doesn't exist.
        """
        if job_id not in self.get_all_job_ids():
            return None
        return self.scheduler.remove_job(job_id)

    def add_update_token_holders(self) -> Job:
        """
        Add a job to update token holders.

        :return: The added Job object.
        """
        job_id = tasks.update_token_holders.__name__
        self._delete_job(job_id)
        return self.scheduler.add_job(
            func=tasks.update_token_holders,
            trigger="interval",
            minutes=self.config.scheduler.UPDATE_TOKEN_HOLDERS_INTERVAL,
            id=job_id,
        )

    def add_check_chats_members(self) -> Job:
        """
        Add a job to check chats members.

        :return: The added Job object.
        """
        job_id = tasks.check_chats_members.__name__
        self._delete_job(job_id)
        return self.scheduler.add_job(
            func=tasks.check_chats_members,
            trigger="interval",
            minutes=self.config.scheduler.CHECK_CHAT_MEMBERS_INTERVAL,
            id=job_id,
        )

    def run(self) -> None:
        """
        Start all schedulers.
        """
        for db, scheduler in self.schedulers.items():
            scheduler.start()
            scheduler.add_listener(on_job_error, mask=EVENT_JOB_ERROR)

        self.add_update_token_holders()
        self.add_check_chats_members()

    def shutdown(self) -> None:
        """
        Shutdown all schedulers.
        """
        self._delete_job(tasks.update_token_holders.__name__)
        self._delete_job(tasks.check_chats_members.__name__)

        for db, scheduler in self.schedulers.items():
            scheduler.shutdown()
