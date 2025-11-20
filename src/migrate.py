from config import Config
from model import UserMigration, TrackMigration, CategoryMigration
from model import ArtistMigration, AlbumMigration, PlaylistMigration

if __name__ == "__main__":
    server_config = Config()
    
    if not UserMigration().create():
        print("Error to create table users")
    
    if not TrackMigration().create():
        print("Error to create table tracks")

    if not CategoryMigration().create():
        print("Error to create table categories")

    if not ArtistMigration().create():
        print("Error to create table artists")
    
    if not AlbumMigration().create():
        print("Error to create table albums")
        
    if not PlaylistMigration().create():
        print("Error to create table playlist")