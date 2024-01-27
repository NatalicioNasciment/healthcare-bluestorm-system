from flask_jwt_extended import JWTManager, jwt_required, create_access_token

jwt = JWTManager()


def init_app(app):
    jwt.init_app(app)