from docker.models.containers import Container


def get_container_exit_code(container: Container) -> int:
    return container.attrs['State']['ExitCode']


def is_container_running(container: Container) -> bool:
    return container.attrs['State']['Running']
