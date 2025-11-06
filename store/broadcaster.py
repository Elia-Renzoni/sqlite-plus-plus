from . import db_api
import socket
import threading
import json
import cluster.leader_election as le

txn_queue = list()
latest_txn = 0
txn_exec_results = list()
mutex = threading.Lock

class Result:
    def __init__(self, res, conn):
        self.response = res
        self.socket_channel = conn

    def get_txn_exec_result(self):
        return self.response['body']

    def get_socket_channel(self):
        return self.socket_channel

# TODO -> this function is useful only if the process
# run in a multithreaded environment, in case of a single thread
# environment the function can be crossed.
def create_and_push_txn(sql_stmt):
    txn_task = db_api.Txn(latest_txn + 1, txn)
    latest_txn += 1
    txn_queue.push(txn_task)

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
            try:
                mutex.acquire()
                txn_exec_results.add(Result(res, net))
            except:
                pass
            finally:
                mutex.release()
        t = threading.Thread(target=do_send(txn, node))
        t.start()
    t.join()

    leader_result = db_api.run_transaction(txn)
    decision = take_decision(leader_result)
    if decision == "commit":
        forward_decision(make_commit_message())
        return decision

    forward_decision(make_rollback_message())
    return decision

def take_decision(leader_result):
    if leader_result == "rollback":
        return "rollback"

    for txn_result in txn_exec_results:
        if txn_result.get_txn_exec_result() == "rollback":
            return "rollback"

    return "commit"

def forward_decision(decision_message):
    for txn_result in txn_exec_result:
        ch = txn_result.get_socket_channel()
        ch.send(decision_message)
        ch.close()

def make_transaction_message(txn):
    return {
            "type": 5,
            "term": le.term_manager.get_term(),
            "body": txn
    }

def make_commit_message():
    return {
            "type": 5,
            "body": "commit"
    }

def make_rollback_message():
    return {
            "type": 5,
            "body": "rollback"
    }
