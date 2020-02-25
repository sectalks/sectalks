# simple redis client
import redis


class MSSClient():
    def __init__(self):
        self.r = redis.Redis(host="redis", port=6379, db=0)

    def get(self, key):
        ret = self.r.get(key)
        if ret is None:
            return ""
        return ret.decode("utf-8")

    def set(self, key, value, expires=None):
        if expires:
            self.r.set(key, value, ex=expires)
        else:
            self.r.set(key, value)
