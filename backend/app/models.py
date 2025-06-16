from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime

class User(SQLModel):
    username: str
    hashed_password: str

class UserTable(User, table=True):
    __tablename__="user"
    id: int | None = Field(default=None, primary_key=True)
    
class Task(SQLModel):
    user_id: int = Field(foreign_key="user.id")  
    created_at: datetime = Field(default_factory=datetime.utcnow) 
    title: str = Field(max_length=200)   
    status: str = Field(default="todo", max_length=20)

class TaskUpdated(SQLModel):
    title: str  | None= Field(default=None, max_length=200) 
    status: str  | None= Field(default=None, max_length=20)

class TaskTable(Task, table=True):
    __tablename__="task"
    id: int | None = Field(default=None, primary_key=True)  

class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


    

