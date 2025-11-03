from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class User(AbstractModel):
    def __init__(self, username: str, email: str, password: str, id: UUID = uuid4()) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.password = password
    
    def save(self) -> bool:
        return True
    
    def update(self, **kwargs):
        return True
    
    @classmethod
    def find_by_id(_class, id):
        return None
    
    @classmethod
    def find_by_attributes(_class, id):
        return None
    
class UserMigration(AbstractModelMigration):
    
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE IF NOT EXISTS users (
            user_id CHARACTER(16) NOT NULL PRIMARY KEY,
            user_username VARCHAR(50) NOT NULL,
            user_email VARCHAR(50) NOT NULL UNIQUE,
            user_password VARCHAR(100) NOT NULL
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
        query_define = "DROP TABLE IF NOT EXISTS users;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True