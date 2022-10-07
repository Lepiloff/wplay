from pydantic import BaseModel, EmailStr, validator

from fastapi import Form

from models.users import Gender


class BaseUser(BaseModel):
    email: EmailStr
    phone: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'

    class Config:
        orm_mode = True


class UserCreateForm(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    password: str
    gender: Gender

    @classmethod
    def as_form(cls, first_name: str = Form(...), last_name: str = Form(...),
                email: str = Form(...), phone: str = Form(...),
                password: str = Form(...), gender: str = Form(...),
                ):
        return cls(
            first_name=first_name, last_name=last_name,
            email=email, phone=phone, gender=gender,
            password=password,
        )
