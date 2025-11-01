import sqlite3

class Txn:
    def __init__(self, txnId, txnJob):
        self.txnId = txnId
        self.txnRun = txnJob

    def get_transation(self):
        return self.txnId, self.txnRun

class Storage:
    def __init__(self):
        self.db_instance = None
        self.db_conn = None
        self.db_cursor = None

    def upgrade_statement(self, sql_stmt):
        pass

    def connect_to(self):
        self.db_conn = sqlite3.connect("instance.db")
        self.db_cursor = self.db_conn.cursor()

    def run_transaction(self, txn):
        try:
            self.db_cursor.executescript(txn)
        except Exception as e:
            self.db_conn.rollback()
