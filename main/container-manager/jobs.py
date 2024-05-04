from checkpointers import CheckpointService
from clients import Client
from clients import ClientPool


class CheckpointJob:
    def __init__(self, client_pool: ClientPool, checkpoint_service: CheckpointService):
        self.client_pool = client_pool
        self.checkpoint_service = checkpoint_service

    def run(self):
        clients: list[Client] = self.client_pool.get_clients()
        for client in clients:
            for container_id in client.container_ids():
                container = client.get_container(container_id)
                if container.status == 'running':
                    self.checkpoint_service.checkpoint(container)
                    self.checkpoint_service.delete_oldest_checkpoint(container)


class RestoreJob:
    def __init__(self, client_pool: ClientPool, checkpoint_service: CheckpointService):
        self.client_pool = client_pool
        self.checkpoint_service = checkpoint_service

    def run(self):
        raise NotImplementedError  # todo
        clients: list[Client] = self.client_pool.get_clients()
        for client in clients:
            for container_id in client.container_ids():
                container = client.get_container(container_id)
                if container.attrs == 'exited':  # exited with error code
                    last_checkpoint = self.checkpoint_service.get_latest_checkpoint()
                    if last_checkpoint:
                        self.checkpoint_service.restore(last_checkpoint)
                    else:
                        pass
                        # todo restart from 0


class DeleteUnusedCheckpointsJob:
    def __init__(self, client_pool: ClientPool, checkpoint_service: CheckpointService):
        self.client_pool = client_pool
        self.checkpoint_service = checkpoint_service

    def run(self):
        raise NotImplementedError  # todo
        clients: list[Client] = self.client_pool.get_clients()
        for client in clients:
            for container_id in client.container_ids():
                container = client.get_container(container_id)
                if container.attrs == 'exited':  # exited with 0 code
                    self.checkpoint_service.delete_all_checkpoints(container)
                    client.remove_container(container_id)
