import sqlite3
import threading
from config import Config
from flask import g

class Database:
    _local = threading.local()

    @staticmethod
    def get_connection():
        if hasattr(Database._local, "conn"):
            return Database._local.conn

        config = Config()

        try:
            conn = sqlite3.connect(
                config.db_filename,
                check_same_thread=True,
                isolation_level=None
            )
            conn.row_factory = sqlite3.Row

            conn.execute("PRAGMA foreign_keys = ON;")

            Database._local.conn = conn

            g.db_conn = conn

        except Exception as e:
            raise ValueError("ERROR TO CREATE OR READ DATABASE") from e

        return conn

    @staticmethod
    def get_cursor():
        conn = Database.get_connection()
        return conn.cursor()
