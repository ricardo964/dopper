from flask import Blueprint, request, jsonify
from time import time_ns
from model import User
from utils import Utils
from service.jsonWebToken import JsonWebToken
from config import Config

jwt = JsonWebToken(Config.jwt_secret)
user_controller = Blueprint("user_controller", __name__, url_prefix='/user')

@user_controller.route("/signup", methods=["POST"])
def signup():
    new_credentials = request.get_json()
    if not Utils.validate_json(
        new_credentials, ["username", "email", "password"]
    ):
        return jsonify({
            "msg": "invalid user data"
        }), 400
    
    try:
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
        
        if new_user.save() is False:
            return jsonify({
                "msg": "Error to create user"
            }), 500

        token = jwt.encode({
            "id": new_user.id.__str__(),
            "_t": time_ns().__str__() 
        })

        return jsonify({
            "msg": "signup successful",
            "token": token
        }), 201

    except Exception as e:
        print(e)
        return jsonify({
            "msg": "bad requests"
        }), 400

@user_controller.route("/signin", methods=["POST"])
def signin():
    credentials = request.get_json()
    if not Utils.validate_json(
            credentials, ["email", "password"]
        ):
        return jsonify({
            "msg": "invalid signin data"
        }), 400
    try:
        user = User.find_by_email(credentials["email"])
        if user is None:
           return jsonify({
                "msg": "user not exits"
            }), 400

        if user.password != credentials["password"]:
            return jsonify({
                "msg": "invalid email or password"
            }), 401
        
        token = jwt.encode({
            "id": user.id.__str__(),
            "_t": time_ns().__str__()
        })

        return jsonify({
            "msg": "signin successful",
            "token": token
        }), 200

    except Exception as e:
        print(e)
        return jsonify({
            "msg": "bad requests"
        }), 400

@user_controller.route("/", methods=["GET"])
def get_user():
    token = request.headers.get("AUTHORIZATION1", None)
    decoded_token = jwt.decode(token)
    if decoded_token is None:
        return jsonify({
            "msg": "invalid token"
        }), 401
    
    try:
        user_data = User.find_by_id(decoded_token["id"])
        if user_data == None:
            return jsonify({
                "msg": "user not exits"
            }), 400
        
        return jsonify({
            "username": user_data.username,
            "email": user_data.email
        }), 200
    except Exception as e:
        print(e)
        return jsonify({
            "msg": "bad requests"
        }), 400

