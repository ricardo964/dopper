from model.AbstractModel import AbstractModel
from model.Artist import Artist
from database.connection import Database
from uuid import UUID, uuid4

class Track(AbstractModel):
    def __init__(self, name: str, duration_in_seconds: int, file_id: str, cover_file_id: str, gen_id = True) -> None:
        if gen_id:  
            self.id = uuid4()
        else:
            self.id = None
        self.name = name
        self.duration_in_seconds = duration_in_seconds
        self.file_id = UUID(file_id)
        self.cover_file_id = UUID(cover_file_id)
        self.artists = list()

    def save(self) -> bool:
        cursor = Database.get_cursor()
        insert_query = """
            INSERT INTO tracks (track_id, track_name, track_duration_in_seconds, track_file_id, track_cover_file_id)
            VALUES (?, ?, ?, ?, ?);
        """
        try:
            cursor.execute(
                insert_query,
                (
                    self.id.__str__(),
                    self.name,
                    self.duration_in_seconds,
                    self.file_id.__str__(),
                    self.cover_file_id.__str__()
                )
            )
        except Exception as e:
            print(f"Error saving track: {e}")
            return False
        finally:
            cursor.close()

        return True
    
    def update_name(self, new_name: str):
        cursor = Database.get_cursor()
        query = "UPDATE tracks SET track_name = ? WHERE track_id = ?;"
        try:
            cursor.execute(query, (new_name, self.id.__str__()))    
        except Exception as e:
            print(f"Error updeting track by id: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    def delete(self):
        cursor = Database.get_cursor()
        query = "DELETE FROM tracks WHERE track_id = ?;"
        try:
            cursor.execute(query, (self.id.__str__(),))    
        except Exception as e:
            print(f"Error deleting track by id: {e}")
            return False
        finally:
            cursor.close()
        
        return True
    
    @classmethod
    def find_all(_class, limit: int = 25, offset: int = 0):
        cursor  = Database.get_cursor()
        query_define = """
            SELECT
                track_id,
                track_name,
                track_duration_in_seconds,
                track_file_id,
                track_cover_file_id,
                artist_id,
                artist_name
            FROM tracks
            LEFT JOIN artists_tracks on tracks.track_id = artists_tracks.at_track_id
            LEFT JOIN artists on artists.artist_id = artists_tracks.at_artist_id
            LIMIT ? OFFSET ?;
        """
        try:
            cursor.execute(query_define, (limit, offset))
            rows = cursor.fetchall()
            
            index =  dict()
            tracks = list()
            
            for id, name, duration, file_id, cover_id, artist_id, artist_name in rows:                    
                if id not in index:
                    track = _class(
                        name,
                        duration,
                        file_id,
                        cover_id,
                        gen_id=False
                    )
                    
                    track.id = UUID(id)
                    tracks.append(track)
                    index[id] = track
                else:
                    track = index[id]
                
                if artist_name is None:
                    continue
                
                artist = Artist(artist_name, gen_id=False)
                artist.id = artist_id
                track.artists.append(artist)
                    
            return tracks
        except Exception as e:
            print(f"Error getting user: {e}")
        finally:
            cursor.close()

        return []

    @classmethod
    def find_by_id(_class, id):
        cursor = Database.get_cursor()
        query_define = f"""
            SELECT * FROM tracks WHERE track_id = ?;
        """
        try:
            cursor.execute(query_define, (id,))
            result = cursor.fetchone()

            if result is not None:
                _id, _name, _duration_in_seconds, _file_id, _cover_file_id = result
                _cls = _class(_name, _duration_in_seconds, _file_id, _cover_file_id, gen_id=False)
                _cls.id = UUID(_id)

                return _cls
        except Exception as e:
            print(f"Error finding track by id: {e}")
        finally:
            cursor.close()

        return None