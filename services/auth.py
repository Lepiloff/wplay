from datetime import datetime, timedelta
from decouple import config
from jose import JWTError, jwt
from passlib.hash import bcrypt

from db import database

from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from models.users import users
from schemas.user_schema import User, Token, UserCreate


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.verify_token(token)


# TODO async ?
class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={
                'WWW-Authenticate': 'Bearer'
            },
        )
        try:
            payload = jwt.decode(
                token,
                config('JWT_SECRET'),
                algorithms=config('JWT_ALGORITHM'),
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')
        try:
            user = users.parse_obj(user_data)
        except ValidationError:
            raise exception from None
        return user

    @classmethod
    async def create_token(cls, user: int) -> Token:
        user_data = await cls.get_user_by_id(pk=user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=int(config('JWT_EXPIRATION'))),
            'sub': str(user_data['id']),
            'user': user_data,
        }
        payload_to_json = jsonable_encoder(payload)
        token = jwt.encode(
            payload_to_json,
            config('JWT_SECRET'),
            algorithm=config('JWT_ALGORITHM'),
        )
        return Token(access_token=token)

    async def register_new_user(self, user_data: UserCreate) -> Token:
        query = users.insert().values(
            email=user_data.email, phone=user_data.phone,
            hashed_password=self.hash_password(user_data.password)
        )
        user_id = await database.execute(query)

        token = await self.create_token(user_id)
        return token

    @classmethod
    async def get_user_by_email(cls, email: str):
        query = users.select().where(users.c.email == email)
        return await database.fetch_one(query)

    @classmethod
    async def get_user_by_id(cls, pk: int):
        #TODO выводить тольео нужные поля в селекте
        query = users.select().where(users.c.id == pk)
        return dict(await database.fetch_one(query))

    async def authenticate_user(self, email: str, password: str,) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        user = dict(await self.get_user_by_email(email=email))
        if not user:
            raise exception
        if not self.verify_password(password, user['hashed_password']):
            raise exception
        return await self.create_token(user['id'])


