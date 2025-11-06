from . import manager as coord
from . import pgroup as pg
import time
import socket
import json
import threading
import asyncio

net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# the base timeout is set to 6s
net.settimeout(6.0)
net.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

suspicious_nodes = set()
mutex = threading.Lock

async def start_detection():
    while True:
        await asyncio.sleep(3)
        items = pg.get_cluster_len()
        if items is 0:
            continue

        nodes = pg.get_cluster_nodes()
        for node in nodes:
            t = threading.Thread(target=ping_node(node))
            t.start()

def ping_node(peer_addr):
    try:
        net.connect(peer_addr)
        net.send(json.dump(make_ping_request()))
        data = net.recv(5048)
        res = json.load(data)
    except socket.timeout:
        update_suspicious_nodes(peer_addr)

def make_ping_request():
    return {
        "type": 2,
        "body": "ping"
    }

def update_suspicious_nodes(peer):
    global suspicious_nodes
    try:
        mutex.acquire()
        has_node: lambda node: node in suspicious_nodes
        if has_node(peer) is not True:
            suspicious_nodes.add(peer)
            return

        suspicious_nodes.discard(peer)
        pg.delete_node(peer)
    except:
        pass
    finally:
        mutex.release()
