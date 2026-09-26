from fastapi import FastAPI
from app.models import Task

app = FastAPI(title="Task Manager API")

tasks = []


@app.get("/")
def root():
    return {"message": "Task Manager API is running"}


@app.post("/tasks")
def create_task(task: Task):
    task_id = len(tasks) + 1

    task_data = {
        "id": task_id,
        **task.model_dump()
    }

    tasks.append(task_data)

    return task_data

@app.get("/tasks")
def get_tasks():
    return tasks