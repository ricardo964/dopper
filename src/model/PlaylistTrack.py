from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class PlaylistTrack(AbstractModel):
    def __init__(self, playlist_id: str, track_id: str) -> None:
        self.playlist_id = UUID(playlist_id)
        self.track_id = UUID(track_id)
    
    def save(self) -> bool:
        cursor = Database.get_cursor()
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
            print(f"Error saving playlists_tracks: {e}")
            return False
        finally:
            cursor.close()
        return True

    @classmethod
    def find_by_id(_class, playlist_id: str, track_id: str):
        cursor = Database.get_cursor()
        query_define = f"""
            SELECT * FROM playlists_tracks WHERE pt_playlist_id = ? AND pt_track_id = ?;
        """
        try:
            cursor.execute(query_define, (playlist_id, track_id))
            result = cursor.fetchone()
            
            if result is not None:
                _artist_id, _track_id = result
                _cls = _class(_artist_id, _track_id)

                return _cls
        except Exception as e:
            print(f"Error finding file by id: {e}")
        finally:
            cursor.close()
        
        return None
    
    def delete(self):
        cursor = Database.get_cursor()
        insert_query = """
            DELETE FROM playlists_tracks
            WHERE pt_playlist_id = ? AND pt_track_id = ?;
        """
        try:
            cursor.execute(
                insert_query,
                (self.playlist_id.__str__(), self.track_id.__str__())
            )
        except Exception as e:
            print(f"Error saving playlists_tracks: {e}")
            return False
        finally:
            cursor.close()

        return True

class PlaylistTrackMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_cursor()
        table_define = """
        CREATE TABLE playlists_tracks (
            pt_playlist_id CHAR(16) NOT NULL,
            pt_track_id CHAR(16) NOT NULL,
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
        cursor = Database.get_cursor()
        query_define = "DROP TABLE playlists_tracks;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()
        return True