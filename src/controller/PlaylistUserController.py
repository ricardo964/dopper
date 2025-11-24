from flask import Blueprint, request, jsonify
from model.Playlist import Playlist
from model.PlaylistTrack import PlaylistTrack
from utils import Utils
from service.jsonWebToken import JsonWebToken
from config import Config

_config = Config()
jwt = JsonWebToken(_config.jwt_secret)
playlist_controller = Blueprint("playlist_controller", __name__, url_prefix='/')

@playlist_controller.route("/playlist", methods=["POST"])
def create_playlist():
    token = request.headers.get("AUTHORIZATION1", None)
    if not token:
        return jsonify({
            "msg": "token header is empty"
        }), 401
    
    decoded_token = jwt.decode(token)
    user_id = decoded_token.get("id", None)
    if user_id is None:
        return jsonify({
            "msg": "invalid token"
        }), 401
    
    new_playlist = request.get_json()
    if not Utils.validate_json(
            new_playlist, ["name"]
        ):
        return jsonify({
            "msg": "invalid playlist data"
        }), 400

    try:
        if Playlist(user_id, new_playlist["name"]).save() is False:
            return jsonify({
                "msg": "Error saving playlist"
            }), 500

        return jsonify({
            "msg": "playlist created"
        }), 201
    except:
        return jsonify({
            "msg": "bad requests"
        }), 400

@playlist_controller.route("/playlist", methods=["GET"])
def get_all_playlist():
    token = request.headers.get("AUTHORIZATION1", None)
    if not token:
        return jsonify({
            "msg": "token header is empty"
        }), 401
    
    decoded_token = jwt.decode(token)
    user_id = decoded_token.get("id", None)
    if user_id is None:
        return jsonify({
            "msg": "invalid token"
        }), 401
    
    try:
        playlists = Playlist.find_all(user_id)

        response = list()
        for playlist in playlists:
            response.append({
                "id": playlist.id,
                "name": playlist.name
            })

        return jsonify({
            "playlists": response
        }), 200
    except:
        return jsonify({
            "msg": "bad requests"
        }), 400

@playlist_controller.route("/playlist/<id>", methods=["GET"])
def get_playlist(id):
    token = request.headers.get("AUTHORIZATION1", None)
    if not token:
        return jsonify({
            "msg": "token header is empty"
        }), 401
    
    decoded_token = jwt.decode(token)
    user_id = decoded_token.get("id", None)
    if user_id is None:
        return jsonify({
            "msg": "invalid token"
        }), 401

    try:
        playlist = Playlist.find_by_id(id, user_id)
        respones = {
            "id": playlist.id,
            "name": playlist.name,
            "tracks": [
                {
                    "id": track.id.__str__(),
                    "name": track.name,
                    "duration_in_seconds": track.duration_in_seconds,
                    "cover_file_id": track.cover_file_id.__str__(),
                    "file_id": track.file_id.__str__(),
                    "artists": [
                        {
                            "id": artist.id.__str__(),
                            "name": artist.name
                        } for artist in track.artists
                    ]
                } for track in playlist.tracks
            ]
        }
        print(playlist.tracks)
        return jsonify({
            "playlist": respones
        }), 200
    except:
        return jsonify({
            "msg": "bad requests"
        }), 400

@playlist_controller.route("/playlist/<id>", methods=["PUT"])
def update_name_playlist(id):
    token = request.headers.get("AUTHORIZATION1", None)
    if not token:
        return jsonify({
            "msg": "token header is empty"
        }), 401
    
    decoded_token = jwt.decode(token)
    user_id = decoded_token.get("id", None)
    if user_id is None:
        return jsonify({
            "msg": "invalid token"
        }), 401
    
    new_playlist = request.get_json()
    if not Utils.validate_json(
            new_playlist, ["name"]
        ):
        return jsonify({
            "msg": "invalid playlist data"
        }), 400
    
    try:
        playlist = Playlist.find_by_id(id, user_id)
        if playlist is None:
            return jsonify({
                "msg": "playlist not exits"
            }), 400
            
        if playlist.update_name(new_playlist["name"]) is None:
            return jsonify({
                "msg": "Error updating playlist "
            }), 400
        
        return jsonify({
            "msg": "playlist updated"
        }), 200
    except:
        return jsonify({
            "msg": "bad requests"
        }), 400

@playlist_controller.route("/playlist/<id>", methods=["DELETE"])
def remove_playlist(id):
    token = request.headers.get("AUTHORIZATION1", None)
    if not token:
        return jsonify({
            "msg": "token header is empty"
        }), 401
    
    decoded_token = jwt.decode(token)
    user_id = decoded_token.get("id", None)
    if user_id is None:
        return jsonify({
            "msg": "invalid token"
        }), 401

    try:
        playlist = Playlist.find_by_id(id, user_id)
        if playlist is None:
            return jsonify({
            "msg": "playlist not exits"
        }), 401
        
        if playlist.delete() is False:
            return jsonify({
                "msg": "Error deleting playlist"
            })
        
        return jsonify({
            "msg": "playlist deleted"
        }), 200
    except:
        return jsonify({
            "msg": "bad requests"
        }), 400

@playlist_controller.route("/playlist/track", methods=["POST"])
def add_track_in_playlist():
    token = request.headers.get("AUTHORIZATION1", None)
    if not token:
        return jsonify({
            "msg": "token header is empty"
        }), 401
    
    decoded_token = jwt.decode(token)
    user_id = decoded_token.get("id", None)
    if user_id is None:
        return jsonify({
            "msg": "invalid token"
        }), 401
    
    new_link = request.get_json()
    print(new_link)
    if not Utils.validate_json(
            new_link, ["track_id", "playlist_id"]
        ):
        return jsonify({
            "msg": "invalid playlist data"
        }), 400

    try:
        if PlaylistTrack(
            new_link["playlist_id"],
            new_link["track_id"]
        ).save() is False:
            return jsonify({
                "msg": "Error adding track in playlist"
            }), 500
        
        return jsonify({
            "msg": "add track in playlist"
        }), 200
    except:
        return jsonify({
            "msg": "bad requests"
        }), 400
    
@playlist_controller.route("/playlist/track", methods=["DELETE"])
def remove_track_in_playlist():
    token = request.headers.get("AUTHORIZATION1", None)
    if not token:
        return jsonify({
            "msg": "token header is empty"
        }), 401
    
    decoded_token = jwt.decode(token)
    user_id = decoded_token.get("id", None)
    if user_id is None:
        return jsonify({
            "msg": "invalid token"
        }), 401
    
    old_link = request.get_json()
    if old_link["track_id"] is None or old_link["playlist_id"]:
        return jsonify({
            "msg": "Error must be track_id and playlist_id"
        }), 400

    try:
        if PlaylistTrack(
            old_link["playlist_id"],
            old_link["track_id"]
        ).delete() is False:
            return jsonify({
                "msg": "Error deleting track in playlist"
            }), 500
        
        return jsonify({
            "msg": "add track in playlist"
        }), 200
    except:
        return jsonify({
            "msg": "bad requests"
        }), 400