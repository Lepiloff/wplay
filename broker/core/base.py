import pika

# TODO почекать с закрытием каналов и логику на это дело добавить какк в примере с pika док


class PikaConnector:
    """
    Synchronous connector to RabbitMq
    """
    SOCKET_TIMEOUT = 5

    def __init__(self, amqp_url):
        self._url = amqp_url
        self._routing_key = None
        self._connection = None
        self._chanel = None

    def connection(self):
        params = pika.URLParameters(self._url)
        params.socket_timeout = self.SOCKET_TIMEOUT
        self._connection = pika.BlockingConnection(params)

    def open_chanel(self):
        self._chanel = self._connection.channel()

    def setup_queue(self, routing_key):
        self._chanel.queue_declare(queue=routing_key)

    def publish(self, routing_key, data):
        self._chanel.basic_publish(exchange='', routing_key=routing_key, body=data)
        self.close()

    def consume(self, routing_key, callback):
        self._chanel.basic_consume(routing_key, callback, auto_ack=True)
        self._chanel.start_consuming()
        self.close()

    def close(self):
        print ('Connection close')
        self._connection.close()

    def run(self, routing_key):
        self.connection()
        self.open_chanel()
        self.setup_queue(routing_key)
