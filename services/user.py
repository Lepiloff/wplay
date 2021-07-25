import itertools
import json

from sqlalchemy import select, desc, column, func, table, and_, text, join

from fastapi import HTTPException
from query import get_profile_info
from db import database


class UserService:

    async def get_user_info(self, pk: int):
        user = await database.fetch_one(query=get_profile_info, values={'pk': pk})
        if user is None:
            raise HTTPException(status_code=404, detail="Events not found")
        user = dict(user.items())
        return user

    async def get_user_evnt(self, pk: int):
        pass
    #TODO  smth like
    # post_list = await database.fetch_all(query=posts.select().where(posts.c.user == user.id))