from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class Artist(AbstractModel):
    def __init__(self, name: str, gen_id=True) -> None:
        if gen_id:
            self.id = uuid4()
        else:
            self.id = None
        self.name = name
    
    def save(self) -> bool:
        cursor = Database.get_cursor()
        insert_query = """
            INSERT INTO artists (artist_id, artist_name)
            VALUES (?, ?);
        """
        try:
            cursor.execute(
                insert_query,
                (self.id.__str__(), self.name)
            )
        except Exception as e:
            print(f"Error saving artist: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    def update_name(self, new_name: str):
        cursor = Database.get_cursor()
        query = "UPDATE artists SET artist_name = ? WHERE artist_id = ?;"
        try:
            cursor.execute(query, (new_name, self.id.__str__()))    
        except Exception as e:
            print(f"Error finding user by id: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    def delete(self):
        cursor = Database.get_cursor()
        query = "DELETE FROM artists WHERE artist_id = ?;"
        try:
            cursor.execute(query, (self.id.__str__(),))    
        except Exception as e:
            print(f"Error finding user by id: {e}")
            return False
        finally:
            cursor.close()
        return True
    
    @classmethod
    def find_all(_class, limit: int = 25, offset: int = 0):
        cursor  = Database.get_cursor()
        query_define = f"""
            SELECT * FROM artists
            LIMIT {limit} OFFSET {offset};
        """
        try:
            cursor.execute(query_define)
            rows = cursor.fetchall()
            
            artists = list()
            for id, name in rows:
                _cls = _class(
                    name,
                    gen_id=False
                )
                
                _cls.id = UUID(id)
                artists.append(_cls)
                
            return artists
        except Exception as e:
            print(f"Error getting artist: {e}")
   
            
        return []
    
    @classmethod
    def find_by_id(_class, id):
        cursor = Database.get_cursor()
        query = "SELECT * FROM artists WHERE artist_id = ?"
        try:
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            
            if result is not None:
                _id, _name = result
                _cls = _class(_name, gen_id=False)
                _cls.id = UUID(_id)

                return _cls     
        except Exception as e:
            print(f"Error finding user by id: {e}")
        finally:
            cursor.close()
        return None

class ArtistMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_cursor()
        table_define = """
        CREATE TABLE artists (
            artist_id CHAR(16) NOT NULL PRIMARY KEY,
            artist_name VARCHAR(50) NOT NULL
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
        cursor = Database.get_cursor()
        query_define = "DROP TABLE artists;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True