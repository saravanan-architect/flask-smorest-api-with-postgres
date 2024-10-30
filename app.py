import os

# import secrets
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app():
    # 1. This create flask app.
    # 2. It helps to run th e flask app

    # app should be file name and also variable name of flask app
    app = Flask(__name__)

    # register blueprint with this api
    # flask configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"  # version of api
    app.config["OPENAPI_VERSION"] = "3.0.3"  # openai version
    app.config["OPENAPI_URL_PREFIX"] = "/"  # flask_smorest root of the api is '/'

    # swagger
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    # Configure DB connection.
    # user = os.getenv("user", "root")
    # password = os.getenv("password", "password")
    # host_name = os.getenv("host_name", "localhost")
    # database = os.getenv("database", "flaskAPI")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    # (
    #     f"mysql+mysqlconnector://{user}:{password}@{host_name}/{database}"
    # )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # it initialize the flask sqlalchemy extension and giving it to our flask app
    db.init_app(app)

    # migrate should be below the db.init_app(app)
    migrate = Migrate(app, db)

    # below code connects the flasks_smorest extensions to flask app
    api = Api(app)

    # secrets.SystemRandom().getrandbits(128) - use to generate secret key, key will be 128 bits long eg: 325437629466322113362707562578973386074
    app.config["JWT_SECRET_KEY"] = "flaskApi"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Signature verification" "failed.",
                    "error": "invalid_token",
                }
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        from flask import jsonify

        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    with app.app_context():
        # Create database tables
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app


create_app()
