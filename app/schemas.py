from pydantic import BaseModel
from typing import Optional


class URLInfo(URL):
    url: str
    admin_url: str


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(User):
    id: int

    class Config:
        orm_mode = True
