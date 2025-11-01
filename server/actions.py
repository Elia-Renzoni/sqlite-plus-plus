from enum import Enum
import cluster.pgroup as pg
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

   if address is None and secretKey is not secret:
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
   if ping is not "ping":
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
   address = le.fetch_leader()
   if leader_addr is None and leader_term is None:
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
        # TODO-> handle db connection and send back the result
        pass

    # TODO-> broadcast the message and take a decision
 

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
      if status_code is 200:
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
