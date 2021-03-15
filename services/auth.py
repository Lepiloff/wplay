from decouple import config
from jose import JWTError, jwt
from passlib.hash import bcrypt

from fastapi import HTTPException, status
from pydantic import ValidationError

from models.users import users
from schemas.user_schema import User, Token


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
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
                algorithm=[config('JWT_ALGORITHM')],
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
    def create_token(cls, user: users) -> Token:
        user_data = User.from_orm(user)
        payload = {

        }


