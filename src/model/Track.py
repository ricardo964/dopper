from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class Track(AbstractModel):
    def __init__(self, name: str, duration_in_seconds: int, mp3_url: str, cover_url: str, id: UUID = uuid4()) -> None:
        self.id = id
        self.name = name
        self.duration_in_seconds = duration_in_seconds
        self.mp3_url = mp3_url
        self.cover_url = cover_url
    
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
    
class TrackMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE IF NOT EXISTS tracks (
            track_id CHARACTER(16) NOT NULL PRIMARY KEY,
            track_name VARCHAR(50) NOT NULL,
            track_duration_in_seconds INT NOT NULL,
            track_mp3_url VARCHAR(100) NOT NULL,
            track_cover_url VARCHAR(100) NOT NULL
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
        query_define = "DROP TABLE IF NOT EXISTS tracks;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True