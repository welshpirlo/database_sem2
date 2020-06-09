import redis
import datetime


class Auth:
    def __init__(self):
        self.conn = redis.Redis(host="127.0.0.1", charset="utf-8", decode_responses=True)

    def signup(self, login):
        if self.conn.hget('users:', login):
            print("This login is already taken. Choose another one")
            self.conn.publish('users', f"{datetime.datetime.now()} - Sign up error - Login is already taken!\n")
            return

        user_id = self.conn.incr('user:id:')
        pipe = self.conn.pipeline(True)
        pipe.hset('users:', login, user_id)
        pipe.hmset('user:%s' % user_id, {
            'login': login,
            'user_id': user_id
        })
        pipe.execute()
        self.conn.publish('users', f"{datetime.datetime.now()} - Sign up success - User {login} registered!\n")
        print("Registered")
        return user_id

    def login(self, login):
        user_id = self.conn.hget("users:", login)
        if not user_id:
            print("No such user")
            self.conn.publish('users',
                                    f"{datetime.datetime.now()} - Log in error - Log in with not existing login\n")
            return -1

        self.conn.sadd("online:", login)
        self.conn.publish('users', f"{datetime.datetime.now()} - Log in success - User {login} signed in!\n")

        return int(user_id)

    def logout(self, login):
        self.conn.publish('users', f"{datetime.datetime.now()} - Log out success - User logged out!\n")
        return self.conn.srem("online:", login)