import redis
import time
from auth import Auth
from message import Messages
from random import randint
from threading import Thread
from faker import Faker


class Spammer(Thread):
    def __init__(self, redis_conn, login, users_list, user_number, auth: Auth):
        Thread.__init__(self)
        self.conn = redis_conn
        self.users_list = users_list
        self.user_number = user_number
        auth.signup(login)
        self.user_id = auth.login(login)
        self.user_login = login

    def run(self):
        messages = Messages()
        while True:
            content = users_set.sentence(nb_words=15, variable_nb_words=True, ext_word_list=None)
            receiver = users[randint(0, 9)]
            messages.create(content, self.user_id, self.conn.hget("users:", receiver))
            print("Message FROM |%s| TO |%s|" % (self.user_login, receiver))
            time.sleep(randint(1, 10))


if __name__ == '__main__':
    threads = []
    users_set = Faker()
    users = [users_set.profile(fields=['username'], sex=None)['username'] for u in range(10)]
    author = Auth()
    for i in range(10):
        print("Username:" + users[i])
        threads.append(Spammer(
            redis.Redis(host="127.0.0.1", charset="utf-8", decode_responses=True),
            users[i], users, 10, author))
    for thread in threads:
        thread.start()

    conn = redis.Redis(host="127.0.0.1", charset="utf-8", decode_responses=True)
    online = conn.smembers("online:")
    for user in online:
        conn.srem("online:", user)