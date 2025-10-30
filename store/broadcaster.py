import db_api
import socket
import threading
import json

txn_queue = list()
db = db_api.Storage()
latest_txn = 0
txn_exec_results = list()

class Result:
    def __init__(self, res, conn):
        self.response = res
        self.socket_channel = conn

    def get_txn_exec_result(self):
        return self.response['body']

    def get_socket_channel(self):
        return self.socket_channel


def create_and_push_txn(sql_stmt):
    txn = db_api.upgrade_statement(sql_stmt)
    txn_task = db_api.Txn(latest_txn + 1, txn)
    latest_txn += 1
    txn_queue.push(txn_task)

def select_txn():
    txn = txn_queue.get(0)
    _, txn_body = txn.get_transaction()
    db.run_transaction(txn_body)

net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
net.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
net.settimout(3.0)
def broadcast_transaction(nodes):
    txn = txn_queue.get(0).get_transaction()
    global txn_exec_results
    for node in nodes:
        def do_send(txn, node_addr):
            net.connect(node_addr)
            net.send(json.dump(make_transaction_message(txn)))

            data = net.recv(5048)
            res = json.load(data)
            txn_exec_results.add(Result(res, net))
        t = threading.Thread(target=do_send(txn, node))
        t.start()
    t.join()
    decision = take_decision()
    if decision is "commit":
        forward_decision(make_commit_message())
        return

    forward_decision(make_rollback_message())

def take_decision():
    for txn_result in txn_exec_results:
        if txn_result.get_txn_exec_result() is "rollback":
            return "rollback"

    return "commit"

def forward_decision(decision_message):
    for txn_result in txn_exec_result:
        ch = txn_result.get_socket_channel()
        ch.send(decision_message)
        ch.close()

def make_transaction_message(txn):
    pass

def make_commit_message():
    pass

def make_rollback_message():
    pass
