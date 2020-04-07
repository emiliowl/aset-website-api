# -*- coding: utf-8 -*-
from os import getenv

class Config:
    SECRET_KEY = getenv('SECRET_KEY') or 'a random string'
    APP_PORT = int(getenv('APP_PORT'))
    DEBUG = eval(getenv('DEBUG').title()),
    MONGODB_SETTINGS = {
        'db': getenv("MONGODB_DB"),
        'host': getenv('MONGODB_HOST'),
        'port': int(getenv("MONGODB_PORT")),
        'username': getenv('MONGODB_USERNAME'),
        'password': getenv('MONGODB_PASSWORD'),
        'authentication_source': getenv("MONGODB_AUTH_SRC")
    }

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
