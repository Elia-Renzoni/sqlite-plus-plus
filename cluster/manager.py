import redis

rdb = redis.Redis(host='localhost', port=6379, decode_responses=True)

def set(key, value):
    return rdb.set(key, value, nx=True)

def get():
    pass

def delete():
    pass
