from model.AbstractModel import AbstractModel
from database.connection import Database
from uuid import UUID, uuid4

class Lyrics(AbstractModel):
    def __init__(self, track_id: str, text: str, lang: str, gen_id = True) -> None:
        if gen_id:
            self.id = uuid4()
        else:
            self.id = None
        
        self.track_id = UUID(track_id)
        self.text = text
        self.lang = lang
    
    def save(self) -> bool:
        cursor = Database.get_cursor()
        insert_query = """
            INSERT INTO lyrics (lyrics_id, lyrics_track_id, lyrics_text, lyrics_lang)
            VALUES (?, ?, ?, ?);
        """
        try:
            cursor.execute(
                insert_query,
                (self.id.__str__(), self.track_id.__str__(), self.text, self.lang)
            )
        except Exception as e:
            print(f"Error saving Lyrics: {e}")
            return False
        finally:
            cursor.close()
        
        return True
    
    @classmethod
    def find_by_id(_class, id):
        cursor = Database.get_cursor()
        query = "SELECT * FROM lyrics WHERE lyrics_id = ?"
        try:
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result:
                _id, _track_id, _text, _lang = result
                _cls = _class(
                    _track_id,
                    _text,
                    _lang,
                    gen_id=False
                )
                
                _cls.id = UUID(_id)
                return _cls
        except Exception as e:
            print(f"Error finding Lyrics by id: {e}")
        finally:
            cursor.close()
        return None
    
    @classmethod
    def find_by_all(_class):
        cursor = Database.get_cursor()
        query = "SELECT * FROM lyrics"
        try:
            cursor.execute(query)
            rows = cursor.fetchall()    
            
            results = []
            for _id, _track_id, _text, _lang in rows:
                _cls = _class(
                    _track_id,
                    _text,
                    _lang,
                    gen_id=False
                )
                
                _cls.id = UUID(_id)
                results.append(_cls)
            return results
        except Exception as e:
            print(f"Error finding Lyrics all: {e}")
            return []
        finally:
            cursor.close()