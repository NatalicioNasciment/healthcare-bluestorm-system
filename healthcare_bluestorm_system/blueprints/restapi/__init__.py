from crypt import methods
from flask import Blueprint
from flask_restful import Api

from .resources import  UserAuthenticationResource, PatientListResource, PharmacyListResource, TransactionListResource

bp = Blueprint("restapi", __name__, url_prefix="/api/v1")
api = Api(bp)


def init_app(app):

    api.add_resource(UserAuthenticationResource, "/auth", methods=["POST"])
    api.add_resource(PatientListResource, "/patients", methods=["GET"])
    api.add_resource(PharmacyListResource, "/pharmacies", methods=["GET"])
    api.add_resource(TransactionListResource, "/transactions", methods=["GET"])

    app.register_blueprint(bp)
