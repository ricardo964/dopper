from flask import Flask, g
from config import Config
Config.load()

from controller.UserController import user_controller
from controller.TrackController import track_controller
from controller.ArtistController import artist_controller
from controller.PlaylistUserController import playlist_controller

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(user_controller)
    app.register_blueprint(track_controller)
    app.register_blueprint(artist_controller)
    app.register_blueprint(playlist_controller)
    
    @app.route("/keep_alive", methods=["GET"])
    def keep_alive():
        return "ok", 200

    @app.teardown_appcontext
    def close_connection(exception):
        conn = getattr(g, "db_conn", None)
        if conn:
            conn.close()

    app.run(
        host="0.0.0.0",
        port=Config.port,
        debug=Config.debug_mode,
    )
