from fastapi import FastAPI, HTTPException
from app.models import Task

app = FastAPI(title="Task Manager API")

tasks = []
next_id = 1


@app.get("/")
def root():
    return {"message": "Task Manager API is running"}


@app.post("/tasks")
def create_task(task: Task):
    global next_id

    task_data = {
        "id": next_id,
        **task.model_dump()
    }

    tasks.append(task_data)
    next_id += 1

    return task_data


@app.get("/tasks")
def get_tasks():
    return tasks


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")
