from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from model.Track import Track
from model.Artist import Artist
from uuid import UUID, uuid4

class Playlist(AbstractModel):
    def __init__(self, user_id: str, name: str, gen_id = True) -> None:
        if gen_id:
            self.id = uuid4()
        else:
            self.id = None
        self.user_id = UUID(user_id)
        self.name = name
        self.tracks = list()
            
    def save(self) -> bool:
        cursor = Database.get_connection().cursor()
        insert_query = """
            INSERT INTO playlists (playlist_id, playlist_user_id, playlist_name)
            VALUES (?, ?, ?);
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
    
    def delete(self):
        cursor = Database.get_connection().cursor()
        insert_query = """
            DELETE FROM playlists
            WHERE playlist_id = ?;
        """
        try:
            cursor.execute(insert_query, (self.id.__str__(),))
        except Exception as e:
            print(f"Error deleting playlist: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    def update_name(self, new_name):
        cursor = Database.get_connection().cursor()
        query = "UPDATE playlists SET playlist_name = ? WHERE playlist_id = ?;"
        try:
            cursor.execute(query, (new_name, self.id.__str__()))    
        except Exception as e:
            print(f"Error updeting playlist by id: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    @classmethod
    def find_all(_class, user_id):
        cursor = Database.get_connection().cursor()
        query = "SELECT * FROM playlists WHERE playlist_user_id = ?"
        try:
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

            playlists = list()
            for id, _user_id, name in rows:
                playlist = _class(
                    _user_id,
                    name,
                    gen_id=False
                )

                playlist.id = id
                playlists.append(playlist)

            return playlists
        except Exception as e:
            print(f"Errpr finding user by id: {e}")
        finally:
            cursor.close()
        return []

    @classmethod
    def find_by_id(_class, id, user_id):
        cursor = Database.get_connection().cursor()
        
        query = """
            SELECT
                playlist_id,
                playlist_user_id,
                playlist_name,
                track_id,
                track_name,
                track_duration_in_seconds,
                track_file_id,
                track_cover_file_id,
                artist_id,
                artist_name
            FROM playlists
            LEFT JOIN playlists_tracks ON playlists.playlist_id = playlists_tracks.pt_playlist_id
            LEFT JOIN tracks ON tracks.track_id = playlists_tracks.pt_track_id
            LEFT JOIN artists_tracks ON tracks.track_id = artists_tracks.at_track_id
            LEFT JOIN artists ON artists.artist_id = artists_tracks.at_artist_id
            WHERE playlists.playlist_id = ? AND playlists.playlist_user_id = ? ORDER BY tracks.track_name;
        """
        
        try:
            cursor.execute(query, (id, user_id))
            rows = cursor.fetchall()
            
            if rows is None:
                return None
            
            (
                _id,
                _user_id,
                _name,
                *_rest
            ) = rows[0]
            
            playlist = _class(_user_id, _name, gen_id=False)
            playlist.id = UUID(_id)
            
            index = dict()
            
            for row in rows:
                (
                    _id,
                    _user_id,
                    _name,
                    _track_id,
                    _track_name,
                    _track_duration_in_seconds,
                    _track_file_id,
                    _track_cover_file_id,
                    _artist_id,
                    _artist_name
                ) = row
                
                if _track_id is None:
                    continue
                
                if _track_id not in index:
                    track = Track(
                        _track_name,
                        _track_duration_in_seconds,
                        _track_file_id,
                        _track_cover_file_id,
                        gen_id=False
                    )
                    track.id = UUID(_track_id)
                    
                    if _artist_id is None:
                        continue
                    
                    artist = Artist(
                        _artist_name,
                        gen_id=False
                    )
                    artist.id = UUID(_artist_id)
                    
                    track.artists.append(artist)
                    playlist.tracks.append(track)
                    index[_track_id] = track
                else:
                    if _artist_id is None:
                        continue
                    artist = Artist(
                        _artist_name,
                        gen_id=False
                    )
                    artist.id = UUID(_artist_id)
                    index[_track_id].artists.append(artist)
            return playlist
        except Exception as e:
            print(f"Error finding user by id: {e}")
        finally:
            cursor.close()
        return None
    
class PlaylistMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE playlists (
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
