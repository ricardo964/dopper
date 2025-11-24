from flask import Blueprint, request, jsonify, send_file
from model.Track import Track
from model.ArtistTrack import ArtistTrack
from model.File import File
from utils import Utils
import io

track_controller = Blueprint("track_controller", __name__, url_prefix='/')

@track_controller.route("/file/<_type>/<id>", methods=["GET"])
def get_file(_type, id):
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
        elif _type == "image":
            mimetype = "image/png"
        else:
            return jsonify({
                "msg": "invalida type"
            }), 400
        
        return send_file(
            men,
            mimetype=mimetype,
        ), 200
        
    except Exception as e:
        print(e)
        return jsonify({
           "msg": "bad request"
        }), 400

@track_controller.route("/track", methods=["GET"])
def get_all_tracks():
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
    except Exception as e:
        print(e)
        return jsonify({
            "msg": "bad request"
        }), 400

@track_controller.route("/track/upload", methods=["POST"])
def upload_track():
    audio_file = request.files.get("audio_file")
    image_file = request.files.get("image_file")
    track_name = request.form.get("name")
    
    if audio_file == "" or image_file == "" or track_name == "":
        return jsonify({
            "msg": "audio_file, image_file or name are required"
        }), 400
    
    if audio_file is None or image_file is None or track_name is None:
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
        track_file_id = _file.id.__str__()
        if _file.save() == False:
            return jsonify({
                "msg": "Error saving audio file"
            }), 500
        
        image_buffer = image_file.read()
        _file = File(len(audio_buffer), image_buffer)
        track_cover_id = _file.id.__str__()
        if  _file.save() is False:
            return jsonify({
                "msg": "Error saving image file"
            }), 500
        
        if Track(
            track_name,
            Utils.get_duration_in_second(audio_buffer),
            track_file_id,
            track_cover_id
        ).save() is False:
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

@track_controller.route("/track/<id>", methods=["PUT"])
def update_track_name(id):
    new_track = request.get_json()
    if not Utils.validate_json(
            new_track, ["name"]
        ):
        return jsonify({
            "msg": "Error must be name"
        }), 400
    
    track = Track.find_by_id(id)
    if track is None:
        return jsonify({
            "msg": "track not exits"
        }), 400
    
    if track.update_name(new_track["name"]) is False:
        return jsonify({
            "msg": "Error updating artist_track"
        }), 500

    return jsonify({
            "msg": "atrack updated"
        }), 201    

@track_controller.route("/track/<id>", methods=["DELETE"])
def remove_track(id):
    try:
        track = Track.find_by_id(id)
        if track is None:
            return jsonify({
                "msg": "track not exits"
            }), 400
        
        if track.delete() is False:
            return jsonify({
                "msg": "Error deleting track"
            }), 500
    
        return jsonify({
                "msg": "track deleted"
            }), 201
    except Exception as e:
        print(e)
        return jsonify({
           "msg": "bad request"
        }), 400

@track_controller.route("/track/add/artist", methods=["POST"])
def add_track_artist():
    new_link = request.get_json()
    if not Utils.validate_json(
            new_link, ["artist_id", "track_id"]
        ):
        return jsonify({
            "msg": "Error must be artist_id and track_id"
        }), 400
    
    try:
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

@track_controller.route("/track/remove/artist", methods=["DELETE"])
def remove_track_artist():
    new_link = request.get_json()
    if not Utils.validate_json(
            new_link, ["artist_id", "track_id"]
        ):
        return jsonify({
            "msg": "Error must be artist_id and track_id"
        }), 400
    
    try:
        artist_track =  ArtistTrack.find_by_id(new_link["artist_id"], new_link["track_id"])
        if artist_track is None:
            return jsonify({
                "msg": "artist_track not exits"
            }), 400
        
        if artist_track.delete() is False:
            return jsonify({
                "msg": "Error deleting artist_track"
            }), 500
    
        return jsonify({
                "msg": "artist_track deleted"
            }), 201
    except Exception as e:
        print(e)
        return jsonify({
           "msg": "bad request"
        }), 400
