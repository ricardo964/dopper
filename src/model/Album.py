from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class Album(AbstractModel):
    def __init__(self, name: str, release_date: str, number_of_songs: int, id: UUID = uuid4()) -> None:
        self.id = id
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
    
class AlbumMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE IF NOT EXISTS albums (
            album_id CHARACTER(16) NOT NUL PRIMARY KEY,
            album_name VARCHAR(50) NOT NULL,
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
        query_define = "DROP TABLE IF NOT EXISTS albums;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True