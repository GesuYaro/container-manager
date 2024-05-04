import docker

from clients import Client
from clients import ClientFactory


class LocalSocketClientFactory(ClientFactory):
    def __init__(self):
        pass

    def create_client(self, **kwargs) -> Client:
        docker_client = docker.from_env()
        return Client(docker_client)

    def factory_type(self) -> str:
        return 'local_socket'
