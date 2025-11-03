from flask import Blueprint, request, jsonify
from model.user import User
from service.jsonWebToken import JsonWebToken
from config import Config

_config = Config()
jwt = JsonWebToken(_config.jwt_secret)
user_controller = Blueprint("user_controller", __name__, url_prefix='/user')


# @user_controller.route("/signup", methods=["POST"])
# def signup():
#     data = request.json
    
#     try:
#         for argv in ["profile_name", "email", "password"]:
#             if argv not in data:
#                 return jsonify({
#                     "msg": f"invalid {argv}"
#                 }), 400
        
#         old_user = User.find_by_email(data["email"])
#         if old_user != None:
#             return jsonify({
#                 "msg": "the user email exits"
#             }), 400
            
#         new_user = User(
#             data["profile_name"],
#             data["email"],
#             data["password"]
#         )
        
#         if not new_user.save():
#             return jsonify({
#                 "msg": "Error to create user"
#             }), 500
        
#         token = jwt.encode({
#             "id": new_user.user_id.__str__()
#         })
        
#         return jsonify({
#             "msg": "user is created",
#             "token": token
#         }), 201
        
#     except:
#         return jsonify({
#             "msg": "bad requests"
#         }), 400

# @user_controller.route("/signin", methods=["POST"])
# def signin():
#     data = request.json
    
#     # try:
#     #     pass
#     # except:
#     #     return jsonify({
#     #         "msg": "Error to crea "
#     #     })
        
#     pass

# @user_controller.route("/", methods=["GET"])
# def get_user():
#     token = request.headers.get("AUTORIZATION", None)
#     if not token:
#         return jsonify({
#             "msg": "token header is empty"
#         }), 401
        
#     try:
#         decoded_token = jwt.decode(token)
#         if not decoded_token.get("id", None):
#             return jsonify({
#                 "msg": "invalid token"
#             }), 401
        
#         data_user = User.find_by_id(decoded_token["id"])
#         if data_user == None:
#             return jsonify({
#                 "msg": "user not exits"
#             }), 400
        
#         return jsonify({
#             "profile_name": data_user.user_profile_name,
#             "email": data_user.user_email
#         }), 400
            
#     except:
#         return jsonify({
#             "msg": "bad requests"
#         }), 400