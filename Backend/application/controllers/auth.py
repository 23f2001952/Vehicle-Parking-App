from flask import current_app as app, jsonify,abort,request
from application.models import User
from flask_jwt_extended import create_access_token,current_user,jwt_required
from werkzeug.security import generate_password_hash,check_password_hash
from application.database import db

def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()

    if not user:
        return jsonify('No user found'),401
    if check_password_hash(user.password,password) == False :
        return jsonify('Incorrect password!'),401
    
    access_token=create_access_token(identity=user)
    return jsonify(access_token=access_token)

def register():

    username = request.json.get("username",None)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    confirm_password = request.json.get("confirm_password",None)

    if not username:
        return jsonify('Username Required'),401
    if not email:
        return jsonify('email Required'),401
    if not password:
        return jsonify('Password Required'),401
    if password != confirm_password:
        return jsonify("Confirm password and passowrd doesn't match"),401
    
    user = User.query.filter_by(username=username).one_or_none()

    if user:
        return jsonify('Username already exists enter an different username'),401
    
    user = User.query.filter_by(email=email).one_or_none()

    if user:
        return jsonify('email already exists enter an different email'),401
    
    db.session.add(User(username=username,email=email,password= generate_password_hash(password)))
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@jwt_required()
def whoami():
    return jsonify( username=current_user.username)