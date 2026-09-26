from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False