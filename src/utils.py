from io import BytesIO
from mutagen.mp3 import MP3

class Utils:
    @staticmethod
    def validate_json(data: dict, required_fields: list[str]) -> bool:
        for field in required_fields:
            if field not in data:
                return False
            if data[field] == "":
                return False
        return True
    
    @staticmethod
    def get_duration_in_second(mp3_bytes: bytes) -> int:
        audio = MP3(BytesIO(mp3_bytes))
        return audio.info.length
    