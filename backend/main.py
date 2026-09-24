import os

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

APP_ENV = os.getenv("APP_ENV", "development")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://taskuser:taskpassword@localhost:5433/taskmanager",
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Task Manager API",
    description=f"Running in {APP_ENV} environment",
)


class Task(BaseModel):
    title: str


@app.get("/")
def root():
    return {"message": "Task Manager API is running"}


@app.get("/tasks")
def get_tasks():
    db = SessionLocal()

    try:
        tasks = db.query(TaskDB).all()

        return [
            {
                "id": task.id,
                "title": task.title,
            }
            for task in tasks
        ]

    finally:
        db.close()


@app.post("/tasks")
def create_task(task: Task):
    db = SessionLocal()

    try:
        new_task = TaskDB(title=task.title)

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return {
            "id": new_task.id,
            "title": new_task.title,
        }

    finally:
        db.close()


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()

    try:
        task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

        if task:
            db.delete(task)
            db.commit()

        return {"message": "Task deleted"}

    finally:
        db.close()