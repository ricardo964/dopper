import os

class Config:
    port: int
    debug_mode: bool
    db_filename: str
    jwt_secret: str
    isLoaded: bool = False
    
    @staticmethod
    def load() -> None:
        if Config.isLoaded == False:
            Config.isLoaded = True
            if not os.getenv("PORT"):
                raise ValueError("PORT NOT PROVIDER")
            Config.port = int(os.getenv("PORT"))

            if os.getenv("DEBUG") not in ["FALSE", "TRUE"]:
                raise ValueError("DEBUG VALUE IS NOT False or True")
            Config.debug_mode = False if os.getenv("DEBUG") == "FALSE" else True

            if not os.getenv("DB_FILENAME"):
                raise ValueError("DB_FILENAME NOT PROVIDER")
            Config.db_filename = os.getenv("DB_FILENAME")

            if not os.getenv("JWT_SECRET"):
                raise ValueError("JWT_SECRET NOT PROVIDER")
            Config.jwt_secret = os.getenv("JWT_SECRET")

        # export PORT=4000
        # export DEBUG=TRUE
        # export DB_FILENAME=filename.db
        # export JWT_SECRET=secret
        
