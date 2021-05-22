import aio_pika
import pickle
import json


async def consume(loop, user_id):
    connection = await aio_pika.connect_robust(
        'amqp://guest:guest@localhost/%2f', loop=loop
    )
    queue_name = f'event_invite_{user_id}'
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name, auto_delete=False)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode('utf8'))
                    print (data)
                    if queue.name in message.body.decode():
                        break