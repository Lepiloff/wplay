import json
import os
import base64
from datetime import timedelta
from datetime import datetime as dt
from decouple import config
from sqlalchemy import select
from passlib.hash import bcrypt

from fastapi import HTTPException, status

from db import database
from helpers.utils import str_to_int
from models.users import users, accounts
from schemas.user_schema import Token, UserCreate
from sessions.core.base import redis_cache
from starlette.requests import Request


async def get_current_user(request: Request):
    exception = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication"
            )
    cookie_authorization: str = request.cookies.get("Authorization")
    if not cookie_authorization:
        raise exception
    session = await redis_cache.hgetall(cookie_authorization)
    if not session:
        raise exception
    return await str_to_int(session)


async def is_authenticated(request: Request):
    cookie_authorization: str = request.cookies.get("Authorization")
    if not cookie_authorization:
        return
    session = await redis_cache.hgetall(cookie_authorization)
    return False if not session else True


# TODO async ?   разобраться с класс методами , нужны ли они тут
class AuthService:

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    async def register_new_user(self, user_data: UserCreate):
        query = users.insert().values(
            email=user_data.email, phone=user_data.phone,
            hashed_password=self.hash_password(user_data.password)
        )
        #TODO тут надо почекать что бы транзакционно создавать обе таблицы
        user_id = await database.execute(query)
        query = accounts.insert().values(user_id=user_id)
        await database.execute(query)
        return user_id

    @classmethod
    async def get_user_by_email(cls, email: str):
        # TODO зачем возвращаем hashed_password
        query = select(users).where(users.c.email == email)
        return await database.fetch_one(query)

    @classmethod
    async def get_user_by_id(cls, pk: int):
        query = select([users.c.id, users.c.hashed_password]).where(users.c.id == pk)
        return dict(await database.fetch_one(query))

    @staticmethod
    async def generate_session_id():
        return base64.b64encode(os.urandom(32))

    async def create_session(self, user_data: dict):
        session_id = await self.generate_session_id()
        return {
              'session_id': str(session_id, 'utf-8'),
              'session_data': {
                  'user_id': user_data['id'],
                  'is_notified': user_data['is_notified']
              }
            }

    async def authenticate_user(self, email: str, password: str):
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        user = await self.get_user_by_email(email=email)
        if not user:
            # TODO messages to user
            raise exception
        user = dict(user)
        if not self.verify_password(password, user['hashed_password']):
            raise exception
        del user['hashed_password']
        return await self.create_session(user)


