from pydantic import BaseModel


class ExecutionRequest(BaseModel):
    image: str
    command: str
