import click
from healthcare_bluestorm_system.ext.database import db
from healthcare_bluestorm_system.ext.auth import create_user
from healthcare_bluestorm_system.models import User


def create_db():
    db.create_all()


def drop_db():
    db.drop_all()


def populate_db():
    data = [
        User(
            id=1, username="teste", password="teste"
        ),
         User(
            id=2, username="teste1", password="teste1"
        )
    ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return User.query.all()


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_db, drop_db, populate_db]:
        app.cli.add_command(app.cli.command()(command))

    # add a single command
    @app.cli.command()
    @click.option('--username', '-u')
    @click.option('--password', '-p')
    def add_user(username, password):
        """Adds a new user to the database"""
        return create_user(username, password)