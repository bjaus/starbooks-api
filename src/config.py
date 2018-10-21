# /src/config.py

import os


class Development(object):
    """
    Development environment confirguration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://bjaus:password@localhost:5432/starbooks')
#    MONGO_DBNAME = os.getenv('MONGO_DBNAME', 'starbooks') #FIXME: remove hard code
#    MONGO_URI = os.getenv('MONGO_URL', 'mongodb://localhost:27017/starbooks') #FIXME: remove hard code
    HOST = 'localhost'
    PORT = 8000


class Production(object):
    """
    Production environment confirguration
    """
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
#    MONGO_DBNAME = os.getenv('MONGO_DBNAME')
#    MONGO_URI = os.getenv('MONGO_URL')
    HOST = 'localhost'
    PORT = 8000


app_config = {
        'development': Development,
        'production': Production,
}

