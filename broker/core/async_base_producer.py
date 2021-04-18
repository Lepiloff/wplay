from pika.exceptions import ChannelClosed, ConnectionClosed
from pika.exchange_type import ExchangeType

from broker.core.async_base import PikaClient

# EXCHANGE = 'message'
# EXCHANGE_TYPE = ExchangeType.topic
# PUBLISH_INTERVAL = 1
# QUEUE = 'text'
# ROUTING_KEY = 'example.text'
# msg = 'test'
# amqp_url = 'amqp://guest:guest@localhost/%2f'


class Publisher(PikaClient):


    def publish(self, msg):
        self.run()
        print('!!!!!!!')
        try:
            print(f'{self.__str__()}.publish(msg), msg = ', msg)
            self.publish_message()
        except ConnectionClosed as e:
            print(f'{self.__str__()} start_publish ConnectionClosed Error: ', e)
            self.connect()
        except ChannelClosed as e:
            print(f'{self.__str__()} start_publish ChannelClosed Error: ', e)
            self.connect()
        except Exception as e:
            print(f'{self.__str__()} start_publish Exception Error: ', e)
            self.connect()
