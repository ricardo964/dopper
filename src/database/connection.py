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
                    _config.db_filename
                )
            except:
                raise ValueError("ERROR TO CREATE OR READ DATABASE")
        return Database.connection
        