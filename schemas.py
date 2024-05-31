from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None

class UserCreate(UserBase):
    username: str
    email: str
    password: str

class User(UserBase):
    id: int
    username: str
    email: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

class FileBase(BaseModel):
    filename: str
    file_type: str

class FileCreate(FileBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str


class File(FileBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
