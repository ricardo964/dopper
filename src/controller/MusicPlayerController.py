from flask import Blueprint, request, jsonify, send_file
from model.Track import Track
from model.File import File
from model.Artist import Artist
from model.ArtistTrack import ArtistTrack
from utils import Utils
from service.jsonWebToken import JsonWebToken
from config import Config
import io

_config = Config()
jwt = JsonWebToken(_config.jwt_secret)
music_player_controller = Blueprint("music_player_controller", __name__, url_prefix='/mp')

#file routes
@music_player_controller.route("/file", methods=["GET"])
def get_file():
    id = request.args.get("id", default=None)
    _type = request.args.get("type", default=None)
    
    # shit code
    if id is None or _type is None:
        return jsonify({
            "msg": "Error must be id and type"
        }), 400
    
    try:
        file = File.find_by_id(id)
        if file is None:
            return jsonify({
                "msg": "id not found"
            }), 400
        
        men = io.BytesIO()
        men.write(file.data)
        men.seek(0)
        
        if _type == "audio":
            mimetype = "audio/mpeg"
        else:
            mimetype = "image/png"
        
        return send_file(
            men,
            mimetype=mimetype,
        ), 200
        
    except:
        return jsonify({
           "msg": "bad request"
        }), 400 

# track routes
@music_player_controller.route("/track", methods=["GET"])
def get_tracks():
    page = request.args.get("page", default=0, type=int)
    try:
        tracks = Track.find_all(limit=25, offset=page * 25)
        
        response = list()
        for track in tracks:
            response.append({
                "id": track.id.__str__(),
                "name": track.name,
                "duration_in_seconds": track.duration_in_seconds,
                "cover_file_id": track.cover_file_id.__str__(),
                "file_id": track.file_id.__str__(),
                "artists": [
                    {
                        "id": artist.id,
                        "name": artist.name    
                    } for artist in track.artists
                ]
            })
        
        return jsonify({
            "tracks": response
        }), 200
    except:
        return jsonify({
            "msg": "bad request"
        }), 400

@music_player_controller.route("/track/upload", methods=["POST"])
def upload_track():
    audio_file = request.files.get("audio_file")
    image_file = request.files.get("image_file")
    track_name = request.form.get("name")
    
    if not audio_file or not image_file or not track_name:
        return jsonify({
            "msg": "audio_file, image_file or name are required"
        }), 400
    
    try:
        if audio_file.content_type != "audio/mpeg":
            return jsonify({
                "msg": "audio_file must be mp3"
            })
            
        audio_buffer = audio_file.read()
        _file = File(len(audio_buffer), audio_buffer)
        track_file_id = _file.id
        if _file.save() is False:
            return jsonify({
                "msg": "Error saving audio file"
            }), 500
        
        image_buffer = image_file.read()
        _file = File(len(audio_buffer), image_buffer)
        track_cover_id = _file.id
        if  _file.save() is False:
            return jsonify({
                "msg": "Error saving image file"
            }), 500
        
        if Track(
            track_name,
            Utils.get_duration_in_second(audio_buffer),
            track_file_id,
            track_cover_id
        ).save() == False:
            return jsonify({
                "msg": "Error saving track"
            }), 500
        
        return jsonify({
            "msg": "upload"
        }), 201

    except:
        return jsonify({
            "msg": "bad request"
        }), 400

# artist routes
@music_player_controller.route("/artist", methods=["POST"])
def create_artist():
    new_artist = request.get_json()
    
    if new_artist["name"] is None:
        return jsonify({
            "msg": "Error must be name"
        }), 400
    
    try:
        if Artist(new_artist["name"]).save() is False:
            return jsonify({
                "msg": "Error saving artist"
            }), 500
    
        return jsonify({
                "msg": "artist created"
            }), 201
    except:
        return jsonify({
           "msg": "bad request"
        }), 400
        
@music_player_controller.route("/artist", methods=["GET"])
def get_artist():
    page = request.args.get("page", default=0, type=int)
    try:
        artists = Artist.find_all(limit=25, offset=page * 25)
        
        response = list()
        for artist in artists:
            response.append({
                "id": artist.id.__str__(),
                "name": artist.name,
            })
    
        return jsonify({
                "artist": response
            }), 201
    except:
        return jsonify({
           "msg": "bad request"
        }), 400

# artist_track
@music_player_controller.route("/artist_track", methods=["POST"])
def link_track_artist():
    new_link = request.get_json()
    
    if new_link["artist_id"] is None and new_link["track_id"] is None:
        return jsonify({
            "msg": "Error must be artist_id and track_id"
        }), 400
    
    try:
        if ArtistTrack.find_by_id(new_link["artist_id"], new_link["track_id"]) is not None:
            return jsonify({
                "msg": "Error exists artist_track"
            }), 400
        
        if ArtistTrack(new_link["artist_id"], new_link["track_id"]).save() is False:
            return jsonify({
                "msg": "Error saving artist_track"
            }), 500
    
        return jsonify({
                "msg": "artist_track created"
            }), 201
    except Exception as e:
        print(e)
        return jsonify({
           "msg": "bad request"
        }), 400