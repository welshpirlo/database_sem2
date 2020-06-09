import redis
import random
import datetime
import time
from threading import Thread


class Worker(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.conn = redis.Redis(host='127.0.0.1', charset="utf-8", decode_responses=True)
        self.delay = random.randint(0, 5)

    def run(self):
        while True:
            message = self.conn.brpop("queue:")
            if message:
                messageID = int(message[1])
                self.conn.hmset('message:%s' % messageID, {'status': 'checking'})
                message = self.conn.hmget("message:%s" % messageID, ["senderID", "receiverID"])
                senderID = int(message[0])
                self.conn.hincrby("user:%s" % senderID, "in_queue", -1)
                self.conn.hincrby("user:%s" % senderID, "checking", 1)
                time.sleep(self.delay)
                is_spam = random.random() > 0.65
                pipe = self.conn.pipeline(True)
                pipe.hincrby("user:%s" % senderID, "checking", -1)
                if is_spam:
                    sender_login = self.conn.hmget("user:%s" % senderID, ["login"])[0]
                    pipe.zincrby("spam:", 1, "user:%s" % sender_login)
                    pipe.hmset('message:%s' % messageID, {'status': 'blocked'})
                    pipe.hincrby("user:%s" % senderID, "blocked", 1)
                    pipe.publish('spam', f"{datetime.datetime.now()} - Spam from user \"%s\""
                                         f"\"%s\"\n" % (
                                            sender_login, self.conn.hmget("message:%s" % messageID, ["content"])[0]))
                else:
                    pipe.hmset('message:%s' % messageID, {'status': 'sent'})
                    pipe.hincrby("user:%s" % senderID, "sent", 1)
                    pipe.sadd("sent:%s" % int(message[1]), messageID)
                pipe.execute()


if __name__ == '__main__':
    for x in range(10):
        worker = Worker()
        worker.daemon = True
        worker.start()
    while True:
        pass