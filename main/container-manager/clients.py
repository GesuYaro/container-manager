from typing import Optional
from abc import ABC, abstractmethod

from docker import DockerClient
from docker.models.containers import Container


class Client:
    def __init__(self, client: DockerClient):
        self.__client = client
        self.__container_ids = []

    def container_count(self) -> int:
        return len(self.__container_ids)

    def container_ids(self) -> list[str]:
        return self.__container_ids

    def add_container(self, image_name: str, command: str) -> str:
        container = self.__client.containers.run(image_name, command=command, detach=True)
        self.__container_ids.append(container.id)
        return container.id

    def get_container(self, container_id: str) -> Container:
        return self.__client.containers.get(container_id)

    def remove_container(self, container_id: str):
        self.__container_ids.remove(container_id)


class ClientPool:
    def __init__(self, clients: Optional[list[Client]] = None):
        if clients is None:
            self.__clients = []
        else:
            self.__clients = clients

    def add_client(self, client: Client):
        self.__clients.append(client)

    def get_clients(self) -> list[Client]:
        return self.__clients


class ClientFactory(ABC):
    @abstractmethod
    def create_client(self, **kwargs) -> Client:
        raise NotImplementedError

    @abstractmethod
    def factory_type(self) -> str:
        raise NotImplementedError
