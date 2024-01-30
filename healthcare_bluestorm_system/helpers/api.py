from flask import abort
from healthcare_bluestorm_system.models import(User)
import jwt
import dynaconf 
import datetime

def validate_headers(headers, *required_keys):
    for key in required_keys:
        if key not in headers:
            abort(400, description=f"Missing header: {key}")

def authenticate_user(token_jwt, uuid):
    user_decoded = jwt.decode(token_jwt, dynaconf.settings.SECRET_KEY, algorithms=['HS256'])
    user = User.query.filter_by(uuid=uuid).first()
    if user is None:
                return abort(
                 code =  404,
                 description ="Result not found."
                )
    if user.uuid != user_decoded.get('id'):
        abort(403, description="Unauthorized: Invalid credentials.")

    current_time = datetime.datetime.now()
    token_expire_time = datetime.datetime.fromtimestamp(user_decoded.get('expire'))

    if token_expire_time < current_time:
        abort(401, description="Token has expired.")