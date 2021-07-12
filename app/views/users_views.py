from operator import ge
import secrets
from http import HTTPStatus

from app.models.models import Profile
from app.views.helpers import add_commit, delete_commit
from flask import Blueprint, jsonify, render_template, request
from flask_httpauth import HTTPDigestAuth, HTTPTokenAuth
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from ipdb import set_trace

bp = Blueprint('users_bp', __name__, url_prefix='/api')

authDigest = HTTPDigestAuth()

@bp.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = Profile.query.filter_by(email=email).first()

    if email != user.email or password != user.password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

@authDigest.get_password
def verify_password(email):
    try:
        user = Profile.query.filter_by(email=email).first()
        return user.password
    except:
        pass

@bp.get('/signup')
def signup_page():
    return render_template('signup.html')

@bp.post('/signup')
def create_profile():
    random_key = secrets.token_urlsafe(16)

    user = Profile(name=request.form['name'], last_name=request.form['last_name'], email=request.form['email'], password=request.form['password'], api_key=random_key)
    add_commit(user)
    return jsonify(user.serialized), 201

@bp.route("/", methods=["DELETE"])
@jwt_required()
def delete():
    logged_user = Profile.query.filter_by(email=get_jwt_identity()).first()
    delete_commit(logged_user)
    return "", HTTPStatus.NO_CONTENT

@bp.route("/", methods=["PUT"])
@jwt_required()
def update():
    data = request.get_json()

    logged_user = Profile.query.filter_by(email=get_jwt_identity()).first()

    for key, value in data.items():
        setattr(logged_user, key, value)

    add_commit(logged_user)

    return {
        "id": logged_user.id,
        "name": logged_user.name,
        "last_name": logged_user.last_name,
        "email": logged_user.email,
    }, HTTPStatus.OK

@bp.route("/", methods=["GET"])
@jwt_required()
def retrieve():
    logged_user = Profile.query.filter_by(email=get_jwt_identity()).first()
    return {"name": logged_user.name, "last_name": logged_user.last_name, "email": logged_user.email}

@bp.route('/logout')
@authDigest.login_required
def logout():
    return "logged out", 401

