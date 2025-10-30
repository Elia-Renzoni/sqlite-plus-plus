import sqlite

class Txn:
    def __init__(self, txnId, txnJob):
        self.txnId = txnId
        self.txnRun = txnJob

    def get_transation(self):
        return self.txnId, self.txnRun

class Storage:
    def __init__(self):
        self.db_instance = None

    def upgrade_statement(self, sql_stmt):
        pass

    def connect_to(self):
        pass

    def run_transaction(self, txn):
        pass
