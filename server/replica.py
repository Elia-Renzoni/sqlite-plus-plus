import json
import socket
import os
import logging
import actions
import sys

HOST = "127.0.0.1"
PORT = 5050
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.settimeout(3.0)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024)
action = actions.Action()

def start():
    listener.bind((HOST, PORT))
    while True:
        conn, _ = listener.accept()
        data = conn.recv(5048)
        handle_conn(conn, data)

def handle_conn(conn, data):
    result = {}
    try:
        req = json.loads(data)
    except json.JSONDecodeError as ex:
        logging.error(ex.msg)
        nack(conn, "Something went wrong while decoding the request")
        return
    
    match req['type']:
        case action.JOIN_CLUSTER:
            result = action.handle_join_cluster(req['body'])
        case action.PING:
            result = action.handle_ping_message(req['body'])
        case action.SQL_STMT:
            result = action.handle_sql_statement(req['body'])
        case action.HEARTBEAT:
            result = action.handle_heartbeat(req['body'])
        case _:
            nack(conn, "Invalid data type")
            return

    context = result.get('ok')
    message = result.get('msg')
    if context is True:
        ack(conn, message)
    else:
        nack(conn, message)

def ack(conn, msg):
    ack_body = {
        "status": 200,
        "ack": msg
    }
    conn.send(json.dumps(ack_body))
    conn.close()

def nack(conn, msg):
    nack_body = {
        "status": 500,
        "nack": msg
    }
    conn.send(json.dumps(nack_body))
    conn.close()

if __name__ == '__main__':
    address = sys.argv[1]
    seed_flag = sys.argv[2]
    secret = sys.argv[3]

    if secret is None and seed_flag is False:
        logging.error("Set a secret for join the cluster")
        sys.exit(1)

    if seed_flag is True:
        actions.perform_seed_registration(address)
    else:
        retries = actions.perform_join_discovery_protocol(address, secret)
        if retries > actions.FAIR_LOSS_RETRIES:
            logging.info("Max retries reached for joining the cluster")
            sys.exit(1)
    logging.info("SQLite++ is ON...")
    start()