from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class PlaylistTrack(AbstractModel):
    def __init__(self, playlist_id: UUID, track_id: UUID) -> None:
        self.playlist_id = playlist_id
        self.track_id = track_id
    
    def save(self) -> bool:
        cursor = Database.get_connection().cursor()
        insert_query = """
            INSERT INTO playlists_tracks (pt_playlist_id, pt_track_id)
            VALUES (?, ?);
        """
        try:
            cursor.execute(
                insert_query,
                (self.playlist_id.__str__(), self.track_id.__str__())
            )
        except Exception as e:
            print(f"Error saving artist-track: {e}")
            return False
        finally:
            cursor.close()
        return True
    
class PlaylistTrackMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE playlists_tracks (
            pt_playlist_id CHAR(16) NOT NULL,
            pt_track_id VARCHAR(50) NOT NULL,
            FOREIGN KEY (pt_playlist_id) REFERENCES playlists(playlist_id),
            FOREIGN KEY (pt_track_id) REFERENCES tracks(track_id),
            PRIMARY KEY (pt_playlist_id, pt_track_id)
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
        query_define = "DROP TABLE playlists_tracks;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True