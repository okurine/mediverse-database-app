# backend/db_connection.py
import mysql.connector
from mysql.connector import pooling
import os

class DB:
    def __init__(self):
        # Read credentials from env vars in production
        self._pool = pooling.MySQLConnectionPool(
            pool_name="mediVerse_pool",
            pool_size=int(os.getenv("DB_POOL_SIZE", "5")),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS", ""),
            database=os.getenv("DB_NAME", "mediVerse"),
            charset="utf8mb4",
            use_pure=True,
            autocommit=False,
        )

    def get_db(self):
        return self._pool.get_connection()

# instantiate once for import usage
db = DB()
