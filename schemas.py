from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    full_name:str
    username:str
    email:str
    password:str

class UserLogin(BaseModel):
    email:str
    password:str