from datetime import datetime
from typing import Optional

from docker.models.containers import Container
from docker.models.checkpoints import Checkpoint


class CheckpointService:
    def __init__(self, datetime_pattern: str = '%Y-%m-%dT%H-%M-%S%z'):
        self.datetime_pattern = datetime_pattern

    def checkpoint(self, container: Container) -> Checkpoint:
        checkpoint_collection = container.get_checkpoints()
        return checkpoint_collection.create(
            container.short_id + '_' + datetime.now().strftime(self.datetime_pattern),
            leave_running=True
        )

    def get_latest_checkpoint(self, container: Container) -> Optional[Checkpoint]:
        checkpoints_by_dates = self.__checkpoints_by_dates(container)
        if len(checkpoints_by_dates) == 0:
            return None
        latest_date = sorted(checkpoints_by_dates.keys(), reverse=True)[0]
        return checkpoints_by_dates[latest_date]

    def restore(self, checkpoint: Checkpoint) -> None:
        checkpoint.client.api.start(
            container=checkpoint.collection.container_id,
            checkpoint=checkpoint
        )

    def delete_all_checkpoints(self, container: Container):
        checkpoints_by_dates = self.__checkpoints_by_dates(container)
        for checkpoint in checkpoints_by_dates.values():
            checkpoint.remove()

    def delete_oldest_checkpoint(self, container: Container):
        checkpoints_by_dates = self.__checkpoints_by_dates(container)
        oldest_date = sorted(checkpoints_by_dates.keys())[0]
        oldest_checkpoint = checkpoints_by_dates[oldest_date]
        oldest_checkpoint.remove()

    def __checkpoints_by_dates(self, container: Container) -> dict[datetime, Checkpoint]:
        checkpoint_collection = container.get_checkpoints()
        return self.__associate_by_date(checkpoint_collection.list())

    def __associate_by_date(self, checkpoints: list[Checkpoint]) -> dict[datetime, Checkpoint]:
        checkpoints_by_date = {}
        for checkpoint in checkpoints:
            date = self.__extract_date(checkpoint)
            if date:
                checkpoints_by_date[date] = checkpoint
        return checkpoints_by_date

    def __extract_date(self, checkpoint: Checkpoint) -> Optional[datetime]:
        date_string = checkpoint.id[13:]  # cut off container_id and '_', get only date part of checkpoint name
        try:
            return datetime.strptime(date_string, self.datetime_pattern)
        except ValueError:
            return None
