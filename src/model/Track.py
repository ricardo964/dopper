from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class Track(AbstractModel):
    def __init__(self, name: str, duration_in_seconds: int, track_file_id: UUID, track_cover_file_id: UUID) -> None:
        self.id = uuid4()
        self.name = name
        self.duration_in_seconds = duration_in_seconds
        self.track_file_id = track_file_id
        self.track_cover_file_id = track_cover_file_id

    def save(self) -> bool:
        return True
    
    def update(self, **kwargs):
        return True
    
    @classmethod
    def find_all(_class, limit: int = 25, offset: int = 0):
        cursor  = Database.get_connection().cursor()
        query_define = f"""
        SELECT
            track_id,
            track_name,
            track_duration_in_seconds,
            track_file_id,
            track_cover_file_id
        FROM tracks
        LIMIT {limit} OFFSET {offset};
        """
        cursor.execute(query_define)
        rows = cursor.fetchall()
        return [Track(**row) for row in rows]

    @classmethod
    def find_by_id(_class, id):
        cursor = Database.get_connection().cursor()
        query_define = f"""
        SELECT
            track_id,
            track_name,
            track_duration_in_seconds,
            track_file_id,
            track_cover_file_id
        FROM tracks
        WHERE track_id = {id};
        """
        cursor.execute(query_define)
        row = cursor.fetchone()
        return Track(**row) if row else None

    @classmethod
    def find_by_attributes(_class, **kwargs):
        cursor = Database.get_connection().cursor()
        query_define = f"""
        SELECT
            track_id,
            track_name,
            track_duration_in_seconds,
            track_file_id,
            track_cover_file_id
        FROM tracks
        WHERE {" AND ".join([f"{key} = {value}" for key, value in kwargs.items()])};
        """
        cursor.execute(query_define)
        rows = cursor.fetchall()
        return [Track(**row) for row in rows] if rows else None
    
class TrackMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE tracks (
            track_id CHAR(16) NOT NULL PRIMARY KEY,
            track_name VARCHAR(50) NOT NULL,
            track_duration_in_seconds INT NOT NULL,
            track_file_id CHAR(16) NOT NULL,
            track_cover_file_id CHAR(16) NOT NULL,
            FOREIGN KEY (track_file_id) REFERENCES files(file_id),
            FOREIGN KEY (track_cover_file_id) REFERENCES files(file_id)
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
        query_define = "DROP TABLE tracks;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True