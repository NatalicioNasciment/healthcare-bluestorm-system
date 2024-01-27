from sqlalchemy import BigInteger, ForeignKey, DateTime 
from healthcare_bluestorm_system.ext.database import db
from sqlalchemy_serializer import SerializerMixin, Serializer
from healthcare_bluestorm_system.ext.serialization import ma
from marshmallow import fields
import datetime



class Patient(db.Model, SerializerMixin,Serializer):
    __tablename__ = 'PATIENTS'

    uuid = db.Column('UUID',db.String(20), primary_key=True)
    first_name = db.Column('FIRST_NAME',db.String(200))
    last_name = db.Column('LAST_NAME',db.String(200))
    date_of_birth = db.Column('DATE_OF_BIRTH',db.DateTime, default=datetime.datetime.utcnow())


    def __init__(self, uuid, first_name, last_name, date_of_birth):
        self.uuid = uuid
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth

class PatientSchema(ma.Schema):
    class Meta:
        fields = ("uuid","first_name","last_name","date_of_birth")



patient_schema = PatientSchema()
patients_schema = PatientSchema(many=True)


class Pharmacy(db.Model, SerializerMixin,Serializer):
    __tablename__ = 'PHARMACIES'
    uuid = db.Column('UUID',db.String(20), primary_key=True)
    name = db.Column('NAME', db.String(200))
    city = db.Column('CITY', db.String(200))
    

    def __init__(self, uuid,  name, city):
        self.uuid = uuid
        self.name = name
        self.city = city

class PharmacySchema(ma.Schema):
    class Meta:
        fields = ("uuid", "name","city")


pharmacy_schema = PharmacySchema()
pharmacies_schema = PharmacySchema(many=True)


class Transaction(db.Model, SerializerMixin,Serializer):
    __tablename__ = 'TRANSACTIONS'
    uuid = db.Column('UUID',db.String, primary_key=True)
    patient_uuid = db.Column('PATIENT_UUID', db.String(200), db.ForeignKey('PATIENTS.UUID'), nullable= False)
    pharmacy_uuid = db.Column('PHARMACY_UUID', db.String(200), db.ForeignKey('PHARMACIES.UUID'), nullable= False)
    amount= db.Column('AMOUNT', db.Numeric(20, 2, True), default=0)
    timestamp = db.Column('TIMESTAMP', db.String(50))

    patient = db.relationship("Patient", backref="PATIENTS", uselist=False)
    pharmacy = db.relationship("Pharmacy", backref="PHARMACIES", uselist=False)
    

    def __init__(self, uuid,  patient_uuid, pharmacy_uuid, amount, timestamp):
        self.uuid = uuid
        self.patient_id = patient_id
        self.pharmacy_id = pharmacy_id
        self.amount = amount
        self.timestamp = timestamp

class TransactionSchema(ma.Schema):
    patient = fields.Nested(PatientSchema, attribute="patient", dump_only=True)
    pharmacy = fields.Nested(PharmacySchema, attribute="pharmacy", dump_only=True)

    class Meta:
        fields = ("uuid", "patient","pharmacy", "amount", "timestamp")

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)



class User(db.Model, SerializerMixin, Serializer):
    __tablename__ = 'USERS'

    uuid = db.Column('UUID',db.Integer, primary_key=True)
    username = db.Column('USERNAME', db.String(500))
    password = db.Column('PASSWORD', db.String(512))

    def __init__(self, uuid:int, username:str, password:str):
        self.uuid = uuid
        self.username = username
        self.password = password


        
