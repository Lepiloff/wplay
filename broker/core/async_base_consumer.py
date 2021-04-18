import json
import time

from broker.core.async_base import PikaClient


class Consumer(PikaClient):

    def __init__(self, io_loop):
        super().__init__(io_loop)
        self.io_loop = io_loop
        self.listeners = set([])

    def handle_message(self, channel, method, header, body):
        try:
            s = str(body, encoding='utf-8')
            msg = json.loads(s, encoding='utf-8', strict=False)
        except ValueError as e:
            print('ValueError:', e)
            msg = {}
        msg['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        for listener in self.listeners:
            listener.write_message(msg)

    # Добавить WebSocket коннектор
    def add_listener(self, listener):
        self.listeners.add(listener)
        print(f'{self.__str__()}: add_listener(listener), listener =', listener)

    # Удаление WebSocket коннекторов
    def remove_listener(self, listener):
        try:
            self.listeners.remove(listener)
            print(f'{self.__str__()}: remove_listener(listener), listener =', listener)
        except KeyError:
            pass
