import datetime
import json
from flask import abort, jsonify,request
import requests
from flask_restful import Resource,reqparse
from sqlalchemy import except_
from healthcare_bluestorm_system.models import(Patient, Pharmacy, Transaction, patients_schema, pharmacies_schema, transactions_schema, User)
from healthcare_bluestorm_system.ext.database import db
import jwt
import dynaconf

SECRET_KEY = dynaconf.settings.SECRET_KEY

class UserAuthenticationResource(Resource):
    def post(self):
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

        token = jwt.encode(payload,SECRET_KEY)
        return jsonify({"id": user.uuid,"token": token, "expire": validity})

class PatientListResource(Resource):

    def get(self):
        try:
            token_jwt =  request.headers.get('token')
            uuid =  request.headers.get('uuid')
            user_decoded =jwt.decode(token_jwt, SECRET_KEY,algorithms=['HS256'])
            user = User.query.filter_by(uuid=uuid).first() 

            date_and_hour_now = datetime.datetime.now() - datetime.timedelta(minutes=1)
            date_and_hour_now = date_and_hour_now.timestamp()
            if user is None:
                return abort(
                 code =  404,
                 description ="Result not found."
                )
            
            elif user.uuid != user_decoded.get('id'):
                return abort(
                code=403,
                description= "you don't have permission to perform this action."
                )
           

            elif user_decoded.get('expire') < date_and_hour_now :
                return abort(
                    code = 401,
                    description =  "You are not allowed to access this route without a token."
                )

            patients = Patient.query.all()
            if len(patients) == 0 :
                return []
            
            return jsonify(patients_schema.dump(patients))
        except Exception as ex:
            abort(code=500,description=ex)

class PharmacyListResource(Resource):

    def get(self):
        try:
            token_jwt =  request.headers.get('token')
            uuid =  request.headers.get('uuid')
            user_decoded =jwt.decode(token_jwt, SECRET_KEY,algorithms=['HS256'])
            user = User.query.filter_by(uuid=uuid).first() 
            
            date_and_hour_now = datetime.datetime.now() - datetime.timedelta(minutes=1)
            date_and_hour_now = date_and_hour_now.timestamp()
            if user is None:
                return abort(
                 code =  404,
                 description ="Result not found."
                )
            
            elif user.uuid != user_decoded.get('id'):
                return abort(
                code=403,
                description= "you don't have permission to perform this action."
                )
           

            elif user_decoded.get('expire') < date_and_hour_now :
                return abort(
                    code = 401,
                    description =  "You are not allowed to access this route without a token."
                )

            pharmacies = Pharmacy.query.all()
            if len(pharmacies) == 0 :
                return []
            return jsonify(pharmacies_schema.dump(pharmacies))
        except ValueError as err:
            abort(code=500,description="Internal server error")

class TransactionListResource(Resource):

    def get(self):
        try:
            token_jwt =  request.headers.get('token')
            uuid =  request.headers.get('uuid')
            user_decoded =jwt.decode(token_jwt, SECRET_KEY,algorithms=['HS256'])
            user = User.query.filter_by(uuid=uuid).first() 
            if user.uuid != user_decoded.get('id'):
                abort(
                code=403,
                description= "you don't have permission to perform this action."
                )
            date_and_hour_now = datetime.datetime.now() - datetime.timedelta(minutes=1)
            date_and_hour_now = date_and_hour_now.timestamp()

            if user_decoded.get('expire') < date_and_hour_now :
                abort(
                    code = 401,
                    description =  "You are not allowed to access this route without a token."
                )

            if user is None:
                abort(
                 code =  404,
                 description ="Result not found."
                )
            
            transactions = Transaction.query.all()
            if len(transactions) == 0 :
                return []
            return jsonify(transactions_schema.dump(transactions))
        except ValueError as err:
            abort(code=500,description="Internal server error")