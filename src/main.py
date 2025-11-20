from flask import Flask
from config import Config

from controller.UserController import user_controller
from controller.MusicPlayerController import music_player_controller

app = Flask(__name__)

if __name__ == "__main__":
    server_config = Config()
    
    app.register_blueprint(user_controller)
    app.register_blueprint(music_player_controller)
    
    app.run(
        host="0.0.0.0",
        port=server_config.port,
        debug=server_config.debug_mode
    )
