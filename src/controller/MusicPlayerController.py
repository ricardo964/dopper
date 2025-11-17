from flask import Blueprint, request, jsonify
from model.Track import Track
from model.File import File
from utils import Utils
from service.jsonWebToken import JsonWebToken
from config import Config

_config = Config()
jwt = JsonWebToken(_config.jwt_secret)
music_player_controller = Blueprint("music_player_controller", __name__, url_prefix='/mp')

# track routes
@music_player_controller.route("/tracks", methods=["GET"])
def get_tracks():
    page = request.args.get("page", default=0, type=int)
    try:
        tracks = Track.find_all(limit=25, offset=page * 25)
        tracks_data = [track.to_dict() for track in tracks]
        return jsonify({
            "tracks": tracks_data
        }), 200
    except:
        return jsonify({
            "msg": "bad request"
        }), 400

@music_player_controller.route("/track/upload", methods=["POST"])
def upload_track():
    audio_file = request.files.get("audio_file")
    image_file = request.files.get("image_file")
    
    if not audio_file or not image_file:
        return jsonify({
            "msg": "audio_file and image_file are required"
        }), 400
    
    try:
        metadata = request.get_json()
        
        audio_buffer = audio_file.read()
        if File(audio_file.content_length, audio_buffer).save() is False:
            return jsonify({
                "msg": "error saving audio file"
            }), 500
        
        image_buffer = image_file.read()
        if File(image_file.content_length, image_buffer).save() is False:
            return jsonify({
                "msg": "error saving image file"
            }), 500

        

    except:
        return jsonify({
            "msg": "bad request"
        }), 400

#playlist routes