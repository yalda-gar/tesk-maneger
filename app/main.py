from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.models import Task
from app.database import get_connection


app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home():
    return {"message": "Task Manager API is running!"}


@app.get("/tasks")
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    connection.close()

    return tasks


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


# WEB INTERFACE


@app.get("/web")
def web_home(request: Request):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    connection.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"tasks": tasks}
    )


@app.post("/web/tasks")
def web_create_task(
    title: str = Form(...),
    description: str = Form("")
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks (title, description, completed)
        VALUES (?, ?, 0)
        """,
        (title, description)
    )

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/web",
        status_code=303
    )


@app.post("/web/tasks/{task_id}/update")
def web_update_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form("")
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET title = ?, description = ?
        WHERE id = ?
        """,
        (title, description, task_id)
    )

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/web",
        status_code=303
    )


@app.post("/web/tasks/{task_id}/delete")
def web_delete_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/web",
        status_code=303
    )


@app.post("/web/tasks/{task_id}/complete")
def web_complete_task(task_id: int):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = CASE
            WHEN completed = 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
        """,
        (task_id,)
    )

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/web",
        status_code=303
    )
