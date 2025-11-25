from model.AbstractModel import AbstractModel
from model.AbstractModelMigration import AbstractModelMigration
from database.connection import Database
from uuid import UUID, uuid4

class File(AbstractModel):
    def __init__(self, size: int, data: bytes, gen_id = True) -> None:
        if gen_id:
            self.id = uuid4()
        else:
            self.id = None
        self.size = size
        self.data = data

    def save(self) -> bool:
        cursor = Database.get_cursor()
        insert_query = """
            INSERT INTO files (file_id, file_size, file_data)
            VALUES (?, ?, ?);
        """
        try:
            cursor.execute(
                insert_query,
                (self.id.__str__(), self.size, self.data)
            )
        except Exception as e:
            print(f"Error saving file: {e}")
            return False
        finally:
            cursor.close()

        return True
    
    def update(self, **kwargs):
        return True

    @classmethod
    def find_by_id(_class, id):
        cursor = Database.get_cursor()
        query_define = f"""
        SELECT * FROM files WHERE file_id = ?;
        """
        try:
            cursor.execute(query_define, (id,))
            result = cursor.fetchone()

            if result is not None:
                _id, _size, _data = result
                _cls = _class(_size, _data, gen_id=False)
                _cls.id = UUID(_id)

                return _cls
        except Exception as e:
            print(f"Error finding file by id: {e}")
        finally:
            cursor.close()

        return None

class FileMigration(AbstractModelMigration):
    def create(self) -> bool:
        cursor = Database.get_cursor()
        table_define = """
        CREATE TABLE files (
            file_id CHAR(16) NOT NULL PRIMARY KEY,
            file_size INT NOT NULL,
            file_data BLOB NOT NULL
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
        query_define = "DROP TABLE files;"
        try:
            cursor.execute(query_define)
        except Exception as e:
            print(f"Error in migration {e}")
            return False
        finally:
            cursor.close()

        return True