from importlib import import_module

from dynaconf import FlaskDynaconf


def load_extensions(app):
    for extension in app.config.get('EXTENSIONS'):
        ext = import_module(extension)
        ext.init_app(app)



def init_app(app, **config):
    FlaskDynaconf(app, **config)
