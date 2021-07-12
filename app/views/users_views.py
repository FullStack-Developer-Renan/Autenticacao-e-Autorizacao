from app.views.helpers import add_commit, delete_commit
from app.models.models import Profile
from flask import Blueprint, render_template, request, jsonify
from flask_httpauth import HTTPDigestAuth, HTTPTokenAuth
from http import HTTPStatus
import secrets

bp = Blueprint('users_bp', __name__, url_prefix='/api')

bp_admin = Blueprint('admin_bp', __name__, url_prefix='/admin')

authDigest = HTTPDigestAuth()

authApi = HTTPTokenAuth(scheme='Bearer')

@bp_admin.route('/')
@authDigest.login_required
def index():
    logged_user = Profile.query.filter_by(email=authDigest.username()).first()
    return {"api_token": logged_user.api_key}

@authApi.verify_token
def verify_token(token):
    try:
        user = Profile.query.filter_by(api_key=token).first()
        return user.api_key
    except:
        pass

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
@authApi.login_required
def delete():
    logged_user = Profile.query.filter_by(api_key=authApi.current_user()).first()
    delete_commit(logged_user)
    return "", HTTPStatus.NO_CONTENT

@bp.route("/", methods=["PUT"])
@authApi.login_required
def update():
    data = request.get_json()

    logged_user = Profile.query.filter_by(api_key=authApi.current_user()).first()

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
@authApi.login_required
def retrieve():
    logged_user = Profile.query.filter_by(api_key=authApi.current_user()).first()
    return {"name": logged_user.name, "last_name": logged_user.last_name, "email": logged_user.email}

@bp.route('/logout')
@authDigest.login_required
def logout():
    return "logged out", 401

