from clients import ClientPool


class TaskExecutor:
    def __init__(self, client_pool: ClientPool):
        self.client_pool = client_pool

    def run_image(self, image_name: str, command: str):
        client = self.__get_available_client()
        container_id = client.add_container(image_name, command)
        return container_id

    def __get_available_client(self):
        clients = self.client_pool.get_clients()
        if len(clients) == 0:
            raise PermissionError
        return min(clients, key=lambda client: client.container_count())
