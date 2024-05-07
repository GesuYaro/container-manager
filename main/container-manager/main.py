from fastapi import FastAPI
import docker

from clients import Client, ClientPool
from task_executors import TaskExecutor
from models import ExecutionRequest
from schedulers import schedule_jobs


app = FastAPI()
docker_client = docker.from_env()
client = Client(docker_client)
client_pool = ClientPool()
client_pool.add_client(client)
task_executor = TaskExecutor(client_pool)
schedule_jobs(client_pool)


@app.post('/task')
def execute_task(request: ExecutionRequest):
    return task_executor.run_image(request.image, request.command)
