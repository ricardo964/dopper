from config import Config
from model import UserMigration, TrackMigration, CategoryMigration
from model import ArtistMigration, AlbumMigration, PlaylistMigration
from model import ArtistTrackMigration, PlaylistTrackMigration, FileMigration

if __name__ == "__main__":
    
    if not FileMigration().create():
        print("Error to create table File")
    
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
        
    if not ArtistTrackMigration().create():
        print("Error to create table playlist")
        
    if not PlaylistTrackMigration().create():
        print("Error to create table playlist")
    