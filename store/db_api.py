import sqlite3
import asyncio
import logging

class Txn:
    def __init__(self, txnId, txnJob):
        self.txnId = txnId
        self.txnRun = txnJob

    def get_transation(self):
        return self.txnId, self.txnRun

PING_STATEMENT = "SELECT 1;"

db_conn = sqlite3.connect("instance.db")
db_cursor = sqlite3.cursor()

def run_transaction(txn):
    try:
        db_cursor.executescript(txn)
    except Exception as e:
        db_conn.rollback()

async def db_pinger():
    while True.
        await asyncio.sleep(3)
        try:
            db_cursor.execute(PING_STATEMENT)
        except sqlite3.Error as e:
            logging.info("database instance is faulty")
