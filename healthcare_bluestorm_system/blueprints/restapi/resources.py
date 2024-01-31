import datetime
import json
from flask import abort, jsonify,request
import requests
from flask_restful import Resource,reqparse
from sqlalchemy import except_
from healthcare_bluestorm_system.models import(Patient, Pharmacy, Transaction, patients_schema, pharmacies_schema, transactions_schema, User)
from healthcare_bluestorm_system.ext.database import db
from healthcare_bluestorm_system.helpers.api import validate_headers, authenticate_user, list_params, filter_model
import jwt
import dynaconf


class UserAuthenticationResource(Resource):
    def post(self):
        validate_headers(request.headers, 'username', 'password')
        username =  request.headers.get('username')
        password =request.headers.get('password')

        user = User.query.filter_by(username=username).first() 
        if user is None:
             return  abort(
                 code =  404,
                 description ="User not found"
                 )
        if user.password != password:
            abort(403,description="Your credentials are incorrect!")
        
        validity = datetime.datetime.now() + datetime.timedelta(minutes=5)
        payload ={
            "id": user.uuid,
            "expire": validity.timestamp()
        }

        token = jwt.encode(payload,dynaconf.settings.SECRET_KEY)
        return jsonify({"id": user.uuid,"token": token, "expire": validity})

class PatientListResource(Resource):

    def get(self):
        try:
            validate_headers(request.headers, 'token', 'uuid')
            token_jwt =  request.headers.get('token')
            uuid =  request.headers.get('uuid')

            authenticate_user(token_jwt, uuid)

            patients = filter_model(Patient, request.args)

            if len(patients) == 0 :
                return []
            
            return jsonify(patients_schema.dump(patients))
        except ValueError as ex:
            abort(code=500,description=ex)

class PharmacyListResource(Resource):

    def get(self):
        try:
            validate_headers(request.headers, 'token', 'uuid')
            token_jwt =  request.headers.get('token')
            uuid =  request.headers.get('uuid')

            authenticate_user(token_jwt, uuid)

            pharmacies = filter_model(Pharmacy, request.args)

            if len(pharmacies) == 0 :
                return []

            return jsonify(pharmacies_schema.dump(pharmacies))
        except ValueError as err:
            abort(code=500,description=err)

class TransactionListResource(Resource):

    def get(self):
        try:
            validate_headers(request.headers, 'token', 'uuid')
            token_jwt =  request.headers.get('token')
            uuid =  request.headers.get('uuid')
           
            authenticate_user(token_jwt, uuid)

            transactions = filter_model(Transaction, request.args)
            
            if len(transactions) == 0 :
                return []
            
            if len(transactions) == 0 :
                return []
            return jsonify(transactions_schema.dump(transactions))
        except ValueError as err:
            abort(code=500,description="Internal server error")