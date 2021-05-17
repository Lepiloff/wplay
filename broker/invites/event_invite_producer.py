import pika, os, logging, json
from broker.core.base import PikaConnector

#TODO  add url to .env
url = 'amqp://guest:guest@localhost/%2f'
# params = pika.URLParameters(url)
# params.socket_timeout = 5
#
# connection = pika.BlockingConnection(params)
#
# channel = connection.channel()
# channel.queue_declare(queue=routing_key)
# channel.basic_publish(exchange='', routing_key=routing_key, body=data)
# print("[X] Message sent to consumer")
# channel.close()
# connection.close()
#
# producer = Publisher(url)
# producer.publish(msg=data)
# producer.publish_message()


class CallPikaConnector:
    def __init__(self):
        self.producer = PikaConnector(url)

    @staticmethod
    def generate_routing_key(to_user_id):
        return f'event.invite.{to_user_id}'

    def send_message(self, to_user_id, data):
        self.producer.run(self.generate_routing_key(to_user_id))
        self.producer.publish(self.generate_routing_key(to_user_id), data)

