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

SECRET_KEY = "bluestorm"

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
        
        validity = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        payload ={
            "id": user.uuid,
            "exp": validity
        }

        token = jwt.encode(payload,SECRET_KEY)
        return jsonify({"id": user.uuid,"token": token, "expire": validity})

class PatientListResource(Resource):

    def get(self):
        try:
            patients = Patient.query.all()
            if len(patients) == 0 :
                return []
            
            return jsonify(patients_schema.dump(patients))
        except Exception as ex:
            abort(code=500,description=ex)

class PharmacyListResource(Resource):

    def get(self):
        try:
            pharmacies = Pharmacy.query.all()
            if len(pharmacies) == 0 :
                return []
            return jsonify(pharmacies_schema.dump(pharmacies))
        except ValueError as err:
            abort(code=500,description="Internal server error")

class TransactionListResource(Resource):

    def get(self):
        try:
            transactions = Transaction.query.all()
            if len(transactions) == 0 :
                return []
            return jsonify(transactions_schema.dump(transactions))
        except ValueError as err:
            abort(code=500,description="Internal server error")