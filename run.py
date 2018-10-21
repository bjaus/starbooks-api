# /run.py

import os
from src.app import create_app
from src.config import app_config


if __name__ == '__main__':
    # handle config
    default = 'development' #FIXME: hard code
    env_name = os.getenv('FLASK_ENV', default)
    config = app_config.get(env_name, default)
    app = create_app(env_name)
    # run app
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )

