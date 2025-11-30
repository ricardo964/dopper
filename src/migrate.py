import sqlite3
from config import Config
Config.load()

tables = [
    """
    CREATE TABLE tracks (
        track_id CHAR(16) NOT NULL PRIMARY KEY,
        track_name VARCHAR(50) NOT NULL,
        track_duration_in_seconds INT NOT NULL,
        track_file_id CHAR(16) NOT NULL,
        track_cover_file_id CHAR(16) NOT NULL,
        FOREIGN KEY (track_file_id) REFERENCES files(file_id) ON DELETE CASCADE,
        FOREIGN KEY (track_cover_file_id) REFERENCES files(file_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE users (
        user_id CHAR(16) NOT NULL PRIMARY KEY,
        user_username VARCHAR(50) NOT NULL,
        user_email VARCHAR(50) NOT NULL UNIQUE,
        user_password VARCHAR(100) NOT NULL
    );
    """,
    """
    CREATE TABLE playlists_tracks (
        pt_playlist_id CHAR(16) NOT NULL,
        pt_track_id CHAR(16) NOT NULL,
        FOREIGN KEY (pt_playlist_id) REFERENCES playlists(playlist_id),
        FOREIGN KEY (pt_track_id) REFERENCES tracks(track_id),
        PRIMARY KEY (pt_playlist_id, pt_track_id)
    );
    """,
    """
    CREATE TABLE playlists (
        playlist_id CHAR(16) NOT NULL PRIMARY KEY,
        playlist_user_id CHAR(16) NOT NULL,
        playlist_name VARCHAR(100) NOT NULL,
        FOREIGN KEY (playlist_user_id) REFERENCES users(user_id)
    );
    """,
    """
    CREATE TABLE files (
        file_id CHAR(16) NOT NULL PRIMARY KEY,
        file_size INT NOT NULL,
        file_data BLOB NOT NULL
    );
    """,
    """
    CREATE TABLE artists_tracks (
        at_artist_id CHAR(16) NOT NULL,
        at_track_id CHAR(16) NOT NULL,
        FOREIGN KEY (at_artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE,
        FOREIGN KEY (at_track_id) REFERENCES tracks(track_id) ON DELETE CASCADE,
        PRIMARY KEY (at_artist_id, at_track_id)
    );
    """,
    """
    CREATE TABLE artists (
        artist_id CHAR(16) NOT NULL PRIMARY KEY,
        artist_name VARCHAR(50) NOT NULL
    );
    """
]

if __name__ == "__main__":
    conn = sqlite3.connect(
        Config.db_filename,
        autocommit=True
    )
    
    for table in tables:
        conn.execute(table)
        conn.commit()

    print("database file was created and tables loaded")

