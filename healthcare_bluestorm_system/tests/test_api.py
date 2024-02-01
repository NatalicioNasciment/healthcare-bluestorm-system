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


def test_successful_authentication(app, client):
    valid_credentials = {'username': 'teste', 'password': 'teste'}

    headers = {'username': valid_credentials['username'], 'password': valid_credentials['password']}
    response = client.post('/api/v1/auth', headers=headers)

    print(app.url_map)
    assert response.status_code == 200

def test_user_not_found(client):
    response = client.post('/api/v1/auth', headers={'username': 'nonexistent', 'password': 'pass'})
    assert response.status_code == 404
    

def test_incorrect_credentials(client):
    response = client.post('/auth', headers={'username': 'user', 'password': 'wrong_pass'})
    assert response.status_code == 403
    

def test_token_generation(client):
    response = client.post('/auth', headers={'username': 'user', 'password': 'pass'})
    assert response.status_code == 200
    

def test_expired_token(client):

    expiration_time = (datetime.datetime.now() - datetime.timedelta(minutes=1)).timestamp()
    response = client.post('/auth', headers={'username': 'user', 'password': 'pass', 'expiration': expiration_time})
    assert response.status_code == 403
    

def test_validation_of_headers(client):
    response = client.post('/auth', headers={})
    assert response.status_code == 400
    

def test_database_error_handling(client, monkeypatch):
    def mock_query(*args, **kwargs):
        raise Exception("Database error")

    monkeypatch.setattr(User, 'query', mock_query)
    
    response = client.post('/auth', headers={'username': 'user', 'password': 'pass'})
    assert response.status_code == 500
    

def test_http_method_handling(client):
    response = client.get('/auth', headers={'username': 'user', 'password': 'pass'})
    assert response.status_code == 405
    

def test_dynamic_token_generation(client, app):
    response = client.post('/auth', headers={'username': 'user', 'password': 'pass'})
    assert response.status_code == 200

    user = User.query.filter_by(username='user').first()
    payload = {"id": user.uuid, "expire": (datetime.datetime.now() + datetime.timedelta(minutes=5)).timestamp()}
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    assert response.json['token'] == token
    


def test_app_is_created(app):
    assert app.name == 'healthcare_bluestorm_system.app'