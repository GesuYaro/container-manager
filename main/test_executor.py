import datetime
import sys
import docker
from docker.models.containers import CheckpointCollection


def parse_argv(argv):
    host = image_name = command = None
    local = False
    for i in range(len(argv)):
        if argv[i] == '--host':
            host = argv[i + 1]
        if argv[i] == '--image-name':
            image_name = argv[i + 1]
        if argv[i] == '--command':
            command = argv[i + 1]
        if argv[i] == '--local':
            local = True

    return host, image_name, local, command


def print_usage_error():
    print('''
    Usage: test_executor.py
    [--local]
    [--host <host>]
    --image-name <image-name>
    [--command <command>]
    ''')


def main():
    if len(sys.argv) < 7:
        host, image_name, local, command = parse_argv(sys.argv)
        if (host is None and not local) or image_name is None:
            print_usage_error()
            return
        client = docker.DockerClient(base_url=host) if not local else docker.from_env()
        print("command: {}".format(command))
        container = client.containers.run(image_name, command=command, detach=True)
        input("waiting, press enter to continue...")
        print(container.id)
        checkpoint_collection = container.get_checkpoints()
        checkpoint = checkpoint_collection.create(container.short_id + datetime.datetime.now().strftime('_%Y-%m-%dT%H-%M-%S'), leave_running=True)
        input("waiting, press enter to continue...")
        container = client.containers.get(container.id)
        status = container.status
        print("status:", status)
        if status == 'exited':
            client.api.start(container.id, checkpoint=checkpoint)
            # container.start(checkpoint=checkpoint, detach=True)
            print('restored')
    else:
        print_usage_error()
        return


main()
