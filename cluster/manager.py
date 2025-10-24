import redis

rdb = redis.Redis(host='localhost', port=6379, decode_responses=True)

def set(key, value):
    return rdb.set(key, value, nx=True)

def get(key):
    return rdb.get(key).decode()

def delete():
    pass

def append(id, value):
    return rdb.sadd(id, value)

def fetch_all(id):
    return rdb.smembers(id)

def count_items(id):
    return rdb.scard(id)

def delete_item(id, value):
    return rdb.srem(id, value)
