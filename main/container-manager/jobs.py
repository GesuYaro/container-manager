from checkpointers import CheckpointService
from clients import Client
from clients import ClientPool
from utils import get_container_exit_code
from utils import is_container_running


restart_codes = range(1, 200)


class CheckpointJob:
    def __init__(self, client_pool: ClientPool, checkpoint_service: CheckpointService):
        self.client_pool = client_pool
        self.checkpoint_service = checkpoint_service

    def run(self):
        clients: list[Client] = self.client_pool.get_clients()
        for client in clients:
            for container_id in client.container_ids():
                container = client.get_container(container_id)
                if is_container_running(container):
                    self.checkpoint_service.checkpoint(container)
                    self.checkpoint_service.delete_oldest_checkpoint(container)


class RestoreJob:
    def __init__(self, client_pool: ClientPool, checkpoint_service: CheckpointService):
        self.client_pool = client_pool
        self.checkpoint_service = checkpoint_service

    def run(self):
        clients: list[Client] = self.client_pool.get_clients()
        for client in clients:
            for container_id in client.container_ids():
                container = client.get_container(container_id)
                if get_container_exit_code(container) in restart_codes:
                    last_checkpoint = self.checkpoint_service.get_latest_checkpoint(container)
                    if last_checkpoint:
                        self.checkpoint_service.restore(last_checkpoint)
                        last_checkpoint.remove()
                    else:
                        pass
                        # todo restart from 0


class DeleteUnusedCheckpointsJob:
    def __init__(self, client_pool: ClientPool, checkpoint_service: CheckpointService):
        self.client_pool = client_pool
        self.checkpoint_service = checkpoint_service

    def run(self):
        clients: list[Client] = self.client_pool.get_clients()
        for client in clients:
            for container_id in client.container_ids():
                container = client.get_container(container_id)
                if get_container_exit_code(container) not in restart_codes:
                    self.checkpoint_service.delete_all_checkpoints(container)
                    client.remove_container(container_id)
