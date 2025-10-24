from enum import Enum
import cluster.manager as coord
import socket

class Action(Enum):
   JOIN_CLUSTER = 1
   PING = 2
   SQL_STMT = 3 
   HEARTBEAT = 4
   DISCOVERY = 5

def handle_join_cluster(req_data):
   pass

def handle_ping_message(req_data):
   pass

def handle_sql_statement(req_data):
   pass

def handle_heartbeat(req_data):
   pass

def perform_seed_registration(seed_addr):
   success = coord.set("seed", seed_addr)
   
   

def perform_join_discovery_protocol():
   pass