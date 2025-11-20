from flask import Blueprint, request, jsonify
from model.User import User
from model.Playlist import Playlist
from utils import Utils
from service.jsonWebToken import JsonWebToken
from config import Config

_config = Config()
jwt = JsonWebToken(_config.jwt_secret)
user_controller = Blueprint("user_controller", __name__, url_prefix='/user')

@user_controller.route("/signup", methods=["POST"])
def signup():
    try:
        new_credentials = request.get_json()
        if not Utils.validate_user_data(new_credentials):
            return jsonify({
                "msg": "invalid user data"
            }), 400
        
        # unefficient
        old_user = User.find_by_email(new_credentials["email"])
        
        if old_user is not None:
            return jsonify({
                "msg": "the user email exists"
            }), 400
        
        new_user = User(
            new_credentials["username"],
            new_credentials["email"],
            new_credentials["password"]
        )
        
        if not new_user.save():
            return jsonify({
                "msg": "Error to create user"
            }), 500

        token = jwt.encode({
            "id": new_user.id.__str__()
        })

        return jsonify({
            "msg": "signup successful",
            "token": token
        }), 201

    except:
        return jsonify({
            "msg": "bad requests"
        }), 400

@user_controller.route("/signin", methods=["POST"])
def signin():
    try:
        credentials = request.get_json()
        if not Utils.validate_signin_data(credentials):
            return jsonify({
                "msg": "invalid signin data"
            }), 400
        
        user = User.find_by_email(credentials["email"])
        if user is None or not user.password == credentials["password"]:
            return jsonify({
                "msg": "invalid email or password"
            }), 401
        
        token = jwt.encode({
            "id": user.id.__str__()
        })

        return jsonify({
            "msg": "signin successful",
            "token": token
        }), 200

    except:
        return jsonify({
            "msg": "bad requests"
        }), 400

@user_controller.route("/", methods=["GET"])
def get_user():
    token = request.headers.get("AUTHORIZATION", None)
    if not token:
        return jsonify({
            "msg": "token header is empty"
        }), 401
    
    try:
        decoded_token = jwt.decode(token)
        if not decoded_token.get("id", None):
            return jsonify({
                "msg": "invalid token"
            }), 401
        
        data_user = User.find_by_id(decoded_token["id"])
        if data_user == None:
            return jsonify({
                "msg": "user not exits"
            }), 400
        
        return jsonify({
            "username": data_user.username,
            "email": data_user.email
        }), 200
    except:
        return jsonify({
            "msg": "bad requests"
        }), 400
