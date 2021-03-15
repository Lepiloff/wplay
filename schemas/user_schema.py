from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str
    phone: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    tocken_type: str = 'bearer'

