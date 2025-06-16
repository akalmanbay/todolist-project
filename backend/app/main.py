from typing import Union
from datetime import datetime

from fastapi import FastAPI, HTTPException
from sqlmodel import select

from database import SessionDep, create_db_and_tables
from models import Task, User, UserTable, TaskTable, TaskUpdated
from routers.auth import router as auth_router


app = FastAPI()

app.include_router(auth_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
   
@app.get("/")
def root():
    return "Root API"

@app.post("/user/add")
def add_user(user: User, session: SessionDep):
    db_user = UserTable(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/task/get/{user_id}")
def get_tasks(user_id: str, session: SessionDep) -> list[Task]:
    tasks = session.exec(select(TaskTable).where(TaskTable.user_id== user_id)).all()
    return tasks

@app.post("/task/add")
def add_task(task:Task, session: SessionDep):
    db_task = TaskTable(**task.model_dump())
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app.post("/task/update/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdated, session: SessionDep):
      
        db_task = session.get(TaskTable, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        task_data = task.model_dump(exclude_unset=True)
        db_task.sqlmodel_update(task_data)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

@app.post("/task/delete/{task_id}", response_model=Task)
def delete_task(task_id: int, session: SessionDep):
        
        db_task = session.get(TaskTable, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        session.delete(db_task)
        session.commit()
        session.refresh(db_task)
        return {"ok": True}

      
        

