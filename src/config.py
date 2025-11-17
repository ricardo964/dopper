import os

# change to singleton later
class Config:
    port: int
    debug_mode: bool
    track_directory: str
    db_filename: str
    jwt_secret: str
    
    
    def __init__(self) -> None:
        if not os.getenv("PORT"):
            raise ValueError("PORT NOT PROVIDER")
        self.port = int(os.getenv("PORT"))

        if os.getenv("DEBUG") not in ["False", "True"]:
            raise ValueError("DEBUG VALUE IS NOT False or True")
        self.debug_mode = True if os.getenv("DEBUG") == "True" else False
        
        if not os.getenv("DB_FILENAME"):
            raise ValueError("DB_FILENAME NOT PROVIDER")
        self.db_filename = os.getenv("DB_FILENAME")
        
        if not os.getenv("JWT_SECRET"):
            raise ValueError("JWT_SECRET NOT PROVIDER")
        self.jwt_secret = os.getenv("JWT_SECRET")
        
        if not os.getenv("TRACK_DIRECTORY"):
            raise ValueError("TRACK_DIRECTORY NOT PROVIDER")
        self.track_directory = os.getenv("TRACK_DIRECTORY")

        # export TRACK_DIRECTORY=./tracks
        # export PORT=4000
        # export DEBUG=True
        # export DB_FILENAME=FILENAME
        # export JWT_SECRET=secret
        