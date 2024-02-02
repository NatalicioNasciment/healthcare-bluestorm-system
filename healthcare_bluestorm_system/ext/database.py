from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def init_app(app):
    db_path = os.path.join(os.getcwd(), 'backend_test.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)
