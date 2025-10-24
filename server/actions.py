from enum import Enum

class Action(Enum):
   JOIN_CLUSTER = 1
   PING = 2
   SQL_STMT = 3 


def handle_join_cluster(req_data):
   pass

def handle_ping_message(req_data):
   pass

def handle_sql_statement(req_data):
   pass