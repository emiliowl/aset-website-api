# -*- coding: utf-8 -*-
from flask import Flask
from config import config

from api import configure_api
from apps.db import db


def create_app(config_name: str) -> Flask:
    app = Flask('api-aset-website')
    app.config.from_object(config[config_name])
    configure_api(app)
    db.init_app(app)

    return app
