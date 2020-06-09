import logging
from threading import Thread

logging.basicConfig(filename="events.log", level=logging.INFO)


class Logger(Thread):
    def __init__(self, conn):
        Thread.__init__(self)
        self.conn = conn

    def run(self):
        listener = self.conn.pubsub()
        listener.subscribe(["users", "spam"])

        for obj in listener.listen():
            if obj['type'] == 'message':
                logging.info(obj['data'])