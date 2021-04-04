import pika, os, logging, json

from_user_id = 1
to_user_id = 2
routing_key=f'event.invite.{to_user_id}'

data = {
        'from_user_id': from_user_id,
        'to_user_id': to_user_id,
        'message': 'Some text'
        }
data = json.dumps(data)
url = 'amqp://guest:guest@localhost/%2f'
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue=routing_key)
channel.basic_publish(exchange='', routing_key=routing_key, body=data)
print("[X] Message sent to consumer")
channel.close()
connection.close()