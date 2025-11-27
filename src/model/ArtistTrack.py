from model.AbstractModel import AbstractModel
from database.connection import Database
from uuid import UUID, uuid4

class ArtistTrack(AbstractModel):
    def __init__(self, artist_id: str, track_id: str) -> None:
        self.artist_id = UUID(artist_id)
        self.track_id = UUID(track_id)
    
    def save(self) -> bool:
        cursor = Database.get_cursor()
        insert_query = """
            INSERT INTO artists_tracks (at_artist_id, at_track_id)
            VALUES (?, ?);
        """
        try:
            cursor.execute(
                insert_query,
                (self.artist_id.__str__(), self.track_id.__str__())
            )
        except Exception as e:
            print(f"Error saving artist-track: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    def delete(self):
        cursor = Database.get_cursor()
        query = "DELETE FROM artists_tracks WHERE at_track_id = ? AND at_artist_id = ?;"
        try:
            cursor.execute(query, (self.track_id.__str__(), self.artist_id.__str__()))    
        except Exception as e:
            print(f"Error deleting artist_track by id: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    @classmethod
    def find_by_id(_class, artist_id, track_id):
        cursor = Database.get_cursor()
        query_define = f"""
            SELECT * FROM artists_tracks WHERE at_track_id = ? AND at_artist_id = ?;
        """
        try:
            cursor.execute(query_define, (track_id, artist_id))
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
