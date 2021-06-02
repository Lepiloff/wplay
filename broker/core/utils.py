from aio_pika import connect, Message, DeliveryMode, ExchangeType, IncomingMessage


def on_message(message: IncomingMessage):
    with message.process():
        print(" [x] %r" % message.body)


async def produce_topic_message(loop, user_id, message_body):
    connection = await connect(
            'amqp://guest:guest@localhost/%2f', loop=loop
    )
    channel = await connection.channel()

    event_join_exchange = await channel.declare_exchange(
        "event_join", ExchangeType.TOPIC
    )

    routing_key = f'event.{user_id}'
    message = Message(
        message_body,
        delivery_mode=DeliveryMode.PERSISTENT
    )
    await event_join_exchange.publish(message, routing_key=routing_key)
    await connection.close()


async def consume_topic_message(loop, user_id):
    connection = await connect(
            'amqp://guest:guest@localhost/%2f', loop=loop
    )
    channel = await connection.channel()
    event_join_exchange = await channel.declare_exchange(
        "event_join", ExchangeType.TOPIC
    )
    queue = await channel.declare_queue(
        "event_queue", durable=True
    )
    binding_key = f'event.{user_id}'
    await queue.bind(event_join_exchange, routing_key=binding_key)
    await queue.consume(on_message)
