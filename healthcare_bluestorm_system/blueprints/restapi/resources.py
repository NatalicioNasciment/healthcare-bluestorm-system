import datetime
import json
from flask import abort, jsonify,request
import requests
from flask_restful import Resource,reqparse
from sqlalchemy import except_
from healthcare_bluestorm_system.models import(Patient, Pharmacy, Transaction, patients_schema, pharmacies_schema, transactions_schema)
from healthcare_bluestorm_system.ext.database import db
import jwt


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