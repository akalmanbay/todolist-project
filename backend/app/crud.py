from fastapi import HTTPException
from sqlmodel import select
from models import UserTable

def get_user(session, username:str):
    user =  session.exec(select(UserTable).where(UserTable.username == username)).first()
    return user
