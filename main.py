from flask import Flask
from models import *

def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename or 'config.py')

    from db import db
    db.init_app(app)
    db.app = app

    db.create_all()

    from views import dashboard
    app.register_blueprint(dashboard)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
