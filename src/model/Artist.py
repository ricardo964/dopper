from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class Artist(AbstractModel):
    def __init__(self, name: str) -> None:
        self.id = uuid4()
        self.name = name
    
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
    

class ArtistMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE artists (
            artist_id CHAR(16) NOT NULL PRIMARY KEY,
            artist_name VARCHAR(50) NOT NULL
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
        query_define = "DROP TABLE artists;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True