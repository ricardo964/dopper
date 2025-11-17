from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class Playlist(AbstractModel):
    def __init__(self, user_id: UUID, name: str) -> None:
        self.id = uuid4()
        self.user_id = user_id
        self.name = name
            
    def save(self) -> bool:
        cursor = Database.get_connection().cursor()
        insert_query = """
            INSERT INTO playlists (playlist_id, playlist_user_id, playlist_name)
            VALUES (%s, %s, %s);
        """
        try:
            cursor.execute(
                insert_query,
                (self.id.__str__(), self.user_id.__str__(), self.name)
            )
        except Exception as e:
            print(f"Error saving playlist: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    def update(self, **kwargs):
        return True
    
    @classmethod
    def find_by_id(_class, id):
        cursor = Database.get_connection().cursor()
        query = "SELECT * FROM playlists WHERE playlist_id = %s"
        try:
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result:
                return _class(*result)
        except Exception as e:
            print(f"Error finding user by id: {e}")
        finally:
            cursor.close()
        return None
    
    @classmethod
    def find_by_attributes(_class, **kwargs):
        cursor = Database.get_connection().cursor()
        query = "SELECT * FROM playlists WHERE "
        query += " AND ".join([f"{key} = %s" for key in kwargs.keys()])
        try:
            cursor.execute(query, tuple(kwargs.values()))
            result = cursor.fetchone()
            if result:
                return _class(*result)
        except Exception as e:
            print(f"Error finding user: {e}")
        finally:
            cursor.close()
        return None
    
class UserMigration(AbstractModelMigration):
    
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE Playlists (
            playlist_id CHAR(16) NOT NULL PRIMARY KEY,
            playlist_user_id CHAR(16) NOT NULL,
            playlist_name VARCHAR(100) NOT NULL,
            FOREIGN KEY (playlist_user_id) REFERENCES users(user_id)
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
        query_define = "DROP TABLE playlists;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()
        return True