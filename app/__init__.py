from flask import Flask
from environs import Env
from app.configs import database, migration
from app import views


def create_app() -> Flask:
    env = Env()
    env.read_env

    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = env("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    database.init_app(app)
    migration.init_app(app)
    views.init_app(app)

    return app
