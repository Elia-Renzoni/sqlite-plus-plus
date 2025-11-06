from enum import Enum
import store.db_api as db
import cluster.pgroup as pg
import store.broadcaster as br
import cluster.leader_election as le
import socket
import json

class Action(Enum):
   JOIN_CLUSTER = 1
   PING = 2
   SQL_STMT = 3 
   HEARTBEAT = 4
   DISCOVERY = 5

def handle_join_cluster(req_data, secret):
   address = req_data['body']
   secretKey = req_data['key']

   if address == None and secretKey != secret:
      return {
         "ok": False,
         "msg": "request empty or corrupted"
      }
   
   pg.add_node(address)
   return {
      "ok": True,
      "msg": "JOIN Approved"
   }
   

def handle_ping_message(req_data):
   ping = req_data['body']
   if ping != "ping":
      return {
         "ok": False,
         "msg": "something went wrong with the body"
      }
   
   return {
      "ok": True,
      "msg": "pong"
   }

def handle_sql_statement(req_data):
   leader_addr = req_data['leader']
   leader_term = req_data['term']
   txn = req_data['body']
   address = le.fetch_leader()
   if leader_addr == None and leader_term == None:
       return {
               "ok": False,
               "msg": "the statement must be sent to the leader address at: " + address
       }
   result = le.check_leader_validity(leader_term)
   if result is not True:
       return {
                "ok": False,
                "msg": "Split Brain, shutdown old leader"
        }
   status = le.fetch_leader_status()
   if status is not True:
       txn_status_result = db.run_transaction(txn)
       if txn_status_result == "commit":
           return {
                   "ok": True,
                   "msg": txn_status_result
           }
       return {
               "ok": False,
               "msg": txn_status_result
       }
   br.create_and_push_txn(txn)
   peers = pg.get_cluster_nodes()
   decision = br.broadcast_transaction(peers)
   if decision == "commit":
        return {
                "ok": True,
                "msg": decision
        }

   return {
            "ok": False,
            "msg": decision
   }
 

def handle_heartbeat(req_data):
   leader_term = req_data['body']
   result = le.check_leader_validity(leader_term)
   if result:
      return {
         "ok": True,
         "msg": "heartbeat arrived, leader is healty"
      }
   
   return {
      "ok": False,
      "msg": "Split Brain, shutdown old leader"
   }

def perform_seed_registration(seed_addr):
    return pg.register_seed(seed_addr)

# the link is based on a fair loss abstraction,
# build on top of exactly-one delivery guaratees
# provided by Redis
FAIR_LOSS_RETRIES = 3

def perform_join_discovery_protocol(nodeAddress, secret):
   seedAddress = pg.retrieve_seed()
   if seedAddress is None:
      return

   # dial the seed node and starts a two-way handshake
   net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   net.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
   net.settimeout(3.0)

   retry = 0
   while retry < FAIR_LOSS_RETRIES:
      net.connect(seedAddress)

      net.send(json.dumps(make_join_message(nodeAddress, secret)))
      data = net.recv(5048)
      res = json.load(data)
      status_code = res['status']
      if status_code == 200:
         net.close()
         break
      retry += 1
   return retry 

def make_join_message(nodeAddress, secret): 
   return {
      "type": 1,
      "body": nodeAddress,
      "key": secret 
   }
