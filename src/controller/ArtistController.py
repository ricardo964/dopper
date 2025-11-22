from flask import Blueprint, request, jsonify
from model.Artist import Artist
from utils import Utils
from service.jsonWebToken import JsonWebToken
from config import Config

_config = Config()
jwt = JsonWebToken(_config.jwt_secret)
artist_controller = Blueprint("artist_controller", __name__, url_prefix='/')

# artist routes
@artist_controller.route("/artist", methods=["POST"])
def create_artist():
    new_artist = request.get_json()
    if not Utils.validate_json(
            new_artist, ["name"]
        ):
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
        
@artist_controller.route("/artist", methods=["GET"])
def get_all_artist():
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
                "artists": response
            }), 201
    except:
        return jsonify({
           "msg": "bad request"
        }), 400

@artist_controller.route("/artist/<id>", methods=["PUT"])
def update_artist_name(id):
    new_artist = request.get_json()
    if not Utils.validate_json(
            new_artist, ["name"]
        ):
        return jsonify({
            "msg": "Error must be name"
        }), 400
    
    try:
        artist = Artist.find_by_id(id)
        if artist is None:
            return jsonify({
                "msg": "artist not exits"
            }), 400
        
        if artist.update_name(new_artist["name"]) is False:
            return jsonify({
                "msg": "error updating artist"
            }), 500
        
        return jsonify({
                "msg": "artist updated"
            }), 201
    except:
        return jsonify({
           "msg": "bad request"
        }), 400

@artist_controller.route("/artist/<id>", methods=["DELETE"])
def remove_artist_name(id):
    try:
        artist = Artist.find_by_id(id)
        if artist is None:
            return jsonify({
                "msg": "artist not exits"
            }), 400
        
        if artist.delete() is False:
            return jsonify({
                "msg": "error deleting artist"
            }), 500
        
        return jsonify({
                "msg": "artist deleted"
            }), 201
    except:
        return jsonify({
           "msg": "bad request"
        }), 400


