from flask import Flask
from environs import Env
from app.configs import database, migration
from app import views
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app() -> Flask:
    env = Env()
    env.read_env

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = env("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "K&nZi3"

    database.init_app(app)
    migration.init_app(app)
    jwt.init_app(app)
    views.init_app(app)

    return app
