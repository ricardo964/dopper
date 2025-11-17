class Utils:
    @staticmethod
    def validate_user_data(data):
        required_fields = ["username", "email", "password"]
        for field in required_fields:
            if field not in data:
                return False
        return True
    
    @staticmethod
    def validate_signin_data(data):
        required_fields = ["email", "password"]
        for field in required_fields:
            if field not in data:
                return False
        return True
    
    @staticmethod
    def validate_track_data(data):
        required_fields = ["track_name", "track_duration_in_seconds", "track_mp3_url", "track_cover_url"]
        for field in required_fields:
            if field not in data:
                return False
        return True