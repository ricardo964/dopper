from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class User(AbstractModel):
    def __init__(self, username: str, email: str, password: str, gen_id = True) -> None:
        if gen_id:
            self.id = uuid4()
        else:
            self.id = None
        
        self.username = username
        self.email = email
        self.password = password
    
    def save(self) -> bool:
        cursor = Database.get_connection().cursor()
        insert_query = """
            INSERT INTO users (user_id, user_username, user_email, user_password)
            VALUES (?, ?, ?, ?);
        """
        try:
            cursor.execute(
                insert_query,
                (self.id.__str__(), self.username, self.email, self.password)
            )
        except Exception as e:
            print(f"Error saving user: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    def update(self, **kwargs):
        return True
    
    @classmethod
    def find_by_id(_class, id):
        cursor = Database.get_connection().cursor()
        query = "SELECT * FROM users WHERE user_id = ?"
        try:
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result:
                _id, _username, _email, _password = result
                _cls = _class(
                    _username,
                    _email,
                    _password,
                    gen_id=False
                )
                
                _cls.id = UUID(_id)
                return _cls
        except Exception as e:
            print(f"Error finding user by id: {e}")
        finally:
            cursor.close()
        return None
    
    @classmethod
    def find_by_email(_class, email):
        cursor = Database.get_connection().cursor()
        query = "SELECT * FROM users WHERE user_email = ?"
        try:
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            if result:
                _id, _username, _email, _password = result
                _cls = _class(
                    _username,
                    _email,
                    _password,
                    gen_id=False
                )
                
                _cls.id = UUID(_id)
                return _cls
        except Exception as e:
            print(f"Error finding user by email: {e}")
        finally:
            cursor.close()
        return None
    
class UserMigration(AbstractModelMigration):
    
    def create(self) -> bool:
        cursor = Database.get_connection().cursor()
        table_define = """
        CREATE TABLE users (
            user_id CHAR(16) NOT NULL PRIMARY KEY,
            user_username VARCHAR(50) NOT NULL,
            user_email VARCHAR(50) NOT NULL UNIQUE,
            user_password VARCHAR(100) NOT NULL
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
        query_define = "DROP TABLE users;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()
        return True