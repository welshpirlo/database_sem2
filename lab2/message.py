import redis


class Messages:
    def __init__(self):
        self.conn = redis.Redis(host="127.0.0.1", charset="utf-8", decode_responses=True)

    def create(self, content, senderID, receiverID):
        if not receiverID:
            print("Message sending error! Receiver doesn't exist!")
            return
        messageID = int(self.conn.incr('message:id:'))
        pipe = self.conn.pipeline(True)
        pipe.hmset('message:%s' % messageID, {
            'status': "created",
            'content': content,
            'messageID': messageID,
            'senderID': senderID,
            'receiverID': receiverID
        })
        pipe.lpush("queue:", messageID)
        pipe.hmset('message:%s' % messageID, {'status': 'in_queue'})
        pipe.zincrby("sent:", 1, "user:%s" % self.conn.hmget("user:%s" % senderID, ["login"])[0])
        pipe.hincrby("user:%s" % senderID, "in_queue", 1)
        pipe.execute()
        return messageID

    def get_all(self, user_id):
        mess_list = self.conn.smembers("sent:%s" % user_id)
        for messageID in mess_list:
            mess = self.conn.hmget("message:%s" % messageID, ["senderID", "content", "status"])
            print("From %s - %s" % (self.conn.hmget("user:%s" % mess[0], ["login"])[0], mess[1]))
            if mess[2] != "delivered":
                pipe = self.conn.pipeline(True)
                pipe.hset("message:%s" % messageID, "status", "delivered")
                pipe.hincrby("user:%s" % mess[0], "sent", -1)
                pipe.hincrby("user:%s" % mess[0], "delivered", 1)
                pipe.execute()