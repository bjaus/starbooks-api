# /src/app.py

import os
from flask import Flask

from .config import app_config
from .models import db


def create_app(env_name):
    """
    Create App
    """

    # app init
    app = Flask(__name__)

    env_name = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(app_config[env_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/', methods=['GET'])
    def index():
        """
        example endpoint
        """
        return ''

    return app

