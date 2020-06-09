import redis
from log import Logger
from auth import Auth
from message import Messages


conn = redis.Redis(host="127.0.0.1", charset="utf-8", decode_responses=True)


def run_admin_interface():
    while True:
        admin_interface()
        number = int(input(">> "))
        if number == 1:
            online = conn.smembers("online:")
            print("Users online:")
            for user in online:
                print(user)
        elif number == 2:
            n = 10
            spammers = conn.zrange("spam:", 0, n - 1, desc=True, withscores=True)
            print("Top %s of most systematic spammers: " % n)
            for index, spammer in enumerate(spammers):
                print(f"{spammer[0]} - {int(spammer[1])} spam messages")
        elif number == 3:
            n = 10
            with open("events.log") as file:
                for line in file.readlines()[-n:]:
                    print(line)
        elif number == 4:
            break
        else:
            print("No such operation\n")


def admin_interface():
    print("-" * 50)
    print("Check info about users")
    print("-" * 50)
    print("|1) Online")
    print("|2) Spammers")
    print("|3) Logs")
    print("|4) Go back")

def run_user_interface():
    author = Auth()
    messages = Messages()
    user_id = -1
    logged_in = False
    listener = Logger(conn)
    listener.setDaemon(True)
    listener.start()

    while True:
        if not logged_in:
            user_interface()
            number = int(input(">> "))
            if number == 1:
                login = input("Enter your login: ")
                author.signup(login)
            elif number == 2:
                login = input("Enter your login: ")
                user_id = author.login(login)
                logged_in = user_id != -1
            elif number == 3:
                break
            else:
                print("No such operation")
        else:
            show_user_func()
            number = int(input(">> "))
            if number == 1:
                mess = input("Write your message: ")
                receiver_login = input("Write the login of person you want to get this message: ")
                receiver = conn.hget("users:", receiver_login)
                if receiver is not None:
                    messages.create(mess, user_id, int(receiver))
                    print("Message sent!")
                else:
                    print("Receiver does not exist!")
            elif number == 2:
                messages.get_all(user_id)
            elif number == 3:
                current = conn.hmget("user:%s" % user_id, ['in_queue', 'checking', 'blocked', 'sent', 'delivered'])
                print("|In queue: %s\n|Is checking: %s\n|Blocked: %s\n|Sent: %s\n|Delivered: %s" % tuple(current))
            elif number == 4:
                login = conn.hmget("user:%s" % user_id, ["login"])[0]
                author.logout(login)
                logged_in = False
                user_id = -1

            else:
                print("No such operation\n")


def user_interface():
    print("-" * 53)
    print("<Log in> or <Sign up> if it is your first time here |")
    print("-" * 53)
    print("|1) <Sign up>")
    print("|2) <Log in>")
    print("|3) Go back")


def show_user_func():
    print("-" * 50)
    print("Send or check new messages here")
    print("-" * 50)
    print("|1) New message")
    print("|2) Received")
    print("|3) Check messages status")
    print("|4) Go back")