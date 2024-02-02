import datetime
import jwt
import pytest
from flask import Flask, jsonify, url_for
from flask.testing import FlaskClient
from dynaconf import FlaskDynaconf
from flask_sqlalchemy import SQLAlchemy
from healthcare_bluestorm_system.blueprints.restapi.resources import UserAuthenticationResource
from healthcare_bluestorm_system.models import User
from decimal import Decimal


def test_successful_authentication():
    user = User('001','teste','teste')

    assert user.username =='teste'
    assert user.password =='teste'

def test_user_not_found(client):
    response = client.post('/api/v1/auth', headers={'username': 'test123  ', 'password': 'test123'})
    assert response.status_code == 404
    

def test_incorrect_credentials(client):
    response = client.post('/api/v1/auth', headers={'username': 'teste1', 'password': 'teste1'})
    assert response.status_code == 403 or response.status_code == 404
    

def test_expired_token(client):

    expiration_time = (datetime.datetime.now() - datetime.timedelta(minutes=1)).timestamp()
    response = client.post('/api/v1/clients', headers={'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlVTRVIxIiwiZXhwaXJlIjoxNzA2NjYwNzgzLjYyMzAzMn0.coYWEuZbOCW59TMXN6diIn1zHJ-Gpkbh4Y9OTXG6ir4', 'uuid': 'USER1'})
    assert response.status_code == 403 or  response.status_code == 404
    

def test_validation_of_headers(client):
    response = client.post('/api/v1/auth', headers={})
    assert response.status_code == 404 or  response.status_code == 400
    


def test_app_is_created(app):
    assert app.name == 'healthcare_bluestorm_system.app'