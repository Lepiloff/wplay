import time
import pika, os, logging, json
from broker.core.base import PikaConnector

# from_user_id = 1
# to_user_id = 2
# routing_key = f'event.invite.{to_user_id}'


def _process_function(msg):
    msg = json.loads(msg)
    print(" [x] Received " + str(msg))
    time.sleep(1)
    print(" PDF processing finished")


def callback(ch, method, properties, body):
    _process_function(body)


url = 'amqp://guest:guest@localhost/%2f'
# params = pika.URLParameters(url)
# params.socket_timeout = 5
#
# connection = pika.BlockingConnection(params)
#
# channel = connection.channel()
# channel.queue_declare(queue=routing_key)
# # channel.basic_publish(exchange='', routing_key='pdfprocess', body='User information')
# channel.basic_consume(routing_key, callback, auto_ack=True)
# channel.start_consuming()
# connection.close()

# if __name__ == '__main__':
#         producer = PikaConnector(url)
#         producer.run(routing_key)
#         producer.consume(routing_key, callback)


class PikaConnectorConsumer:
    def __init__(self):
        self.producer = PikaConnector(url)

    @staticmethod
    def generate_routing_key(to_user_id):
        return f'event.invite.{to_user_id}'

    def get_message(self, to_user_id):
        self.producer.run(self.generate_routing_key(to_user_id))
        self.producer.consume(self.generate_routing_key(to_user_id), callback)
