from pydantic import BaseModel


class Task(BaseModel):
    id: int
    name: str
    description: str
    status: str
