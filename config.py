# configuration file config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = "postgres://postgres:1numan1@localhost"
database_name = '/web_chat_task'

class BaseConfig:
    """Base configuration."""
    DEBUG = False
    SECRET_KEY = 'Secret'
    TOKEN_VAILD_SEC = 86400 #Seconds
    # database settings
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name # For heroku db this becomes url.
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REST_URL_PREFIX = ''
    # User password settings
    KEY_LENGTH = 32
    HASH_FUNCTION = 'sha512'
    COST_FACTOR = 10000

    REST_URL_TESTING = 'http://localhost:5000/'

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
