import jwt
from service.jsonWebToken.AbstractJsonWebToken import AbtractJsonWebToken

class JsonWebToken(AbtractJsonWebToken):
    def __init__(self, secret_key: str, algorithm: str = "HS256") -> None:
        super().__init__()
        self.algorithm = algorithm
        self.secret_key = secret_key
    
    def encode(self, payload: dict) -> str:
        print(self.secret_key)
        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return token
    
    def decode(self, token: str) -> dict:
        try:
            token = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return token
        except:
            return None