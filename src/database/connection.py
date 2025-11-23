import sqlite3
from config import Config

class Database:
    connection = None
    
    @staticmethod
    def get_connection():
        if not Database.connection:
            _config = Config()
            try:
                Database.connection = sqlite3.connect(
                    _config.db_filename,
                    autocommit=True
                )
                
                cursor = Database.connection.cursor()
                cursor.execute("PRAGMA foreign_keys = ON;")
                cursor.close()
                
            except Exception as e:
                raise ValueError("ERROR TO CREATE OR READ DATABASE", e)
        return Database.connection
        