import asyncio

from fastapi import Request

# from broker.core.utils import consume_message
from broker.core.utils import consume_topic_message
from services.auth import is_authenticated


async def rmq_consumer_middleware(request: Request, call_next, ):
    current_user = await is_authenticated(request)
    if current_user:
        print (f'Current user detected : {current_user}')
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(consume_topic_message(loop, current_user))
    response = await call_next(request)
    return response
