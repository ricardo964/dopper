import os

# change to singleton later
class Config:
    port: int
    debug_mode: bool
    db_filename: str
    jwt_secret: str
    
    
    def __init__(self) -> None:
        # if not os.getenv("PORT"):
        #     raise ValueError("PORT NOT PROVIDER")
        self.port = 4000

        # if os.getenv("DEBUG") not in ["False", "True"]:
        #     raise ValueError("DEBUG VALUE IS NOT False or True")
        self.debug_mode = False
        
        # if not os.getenv("DB_FILENAME"):
        #     raise ValueError("DB_FILENAME NOT PROVIDER")
        self.db_filename = "database.db"
        
        # if not os.getenv("JWT_SECRET"):
        #     raise ValueError("JWT_SECRET NOT PROVIDER")
        self.jwt_secret = "SECRET"

        # export PORT=4000
        # export DEBUG=True
        # export DB_FILENAME=FILENAME
        # export JWT_SECRET=secret
        