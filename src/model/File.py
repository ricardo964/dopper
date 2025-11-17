from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class File(AbstractModel):
    def __init__(self, size: int, data: bytes) -> None:
        self.id =  uuid4()
        self.size = size
        self.data = data

    def save(self) -> bool:
        return True
    
    def update(self, **kwargs):
        return True

    @classmethod
    def find_by_id(_class, id):
        cursor = Database.get_connection().cursor()
        query_define = f"""
        SELECT
            file_id,
            file_size,
            file_data
        FROM files
        WHERE file_id = {id};
        """
        cursor.execute(query_define)
        row = cursor.fetchone()
        return File(**row) if row else None

    @classmethod
    def find_by_attributes(_class, **kwargs):
        cursor = Database.get_connection().cursor()
        query_define = f"""
        SELECT
            track_id,
            file_size,
            file_data
        FROM files
        WHERE {" AND ".join([f"{key} = {value}" for key, value in kwargs.items()])};
        """
        cursor.execute(query_define)
        rows = cursor.fetchall()
        return [File(**row) for row in rows] if rows else None

class FileMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE files (
            file_id CHAR(16) NOT NULL PRIMARY KEY,
            file_size INT NOT NULL,
            file_data BLOB NOT NULL
        );
        """
        try:
            cursor.execute(table_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True
    
    def drop(self) -> bool:
        cursor = Database.get_connection().cursor()
        query_define = "DROP TABLE files;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True