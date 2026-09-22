
from fastapi import FastAPI
from app.models import Task
from app.database import get_connection

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Task Manager API is running!"}


@app.get("/test-task")
def test_task():
    task = Task(
        title="Python leren",
        description="FastAPI oefenen"
    )
    return task


# READ
@app.get("/tasks")
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    connection.close()

    return tasks


# CREATE 
@app.post("/tasks")
def create_task(task: Task):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, description, completed)
        VALUES (?, ?, ?)
        """,
        (task.title, task.description, task.completed)
    )

    connection.commit()

    task_id = cursor.lastrowid

    connection.close()

    return {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }


# UPDATE
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?, completed = ?
        WHERE id = ?
        """,
        (task.title, task.description, task.completed, task_id)
    )

    connection.commit()
    connection.close()

    return {
        "id": task_id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }


# DELETE
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Task deleted successfully",
        "id": task_id
    }