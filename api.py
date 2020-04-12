# -*- coding: utf-8 -*-
from flask_cors import CORS
from apps.core.blueprints.therapists import bp as therapists_bp
from apps.core.blueprints.customers import bp as customers_bp
from apps.agenda.blueprints.agenda import bp as agenda_bp


def configure_api(app):
    print('configuring blueprints...')
    app.register_blueprint(therapists_bp, url_prefix='/api/therapists')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(agenda_bp, url_prefix='/api/agendas')
    app.url_map.strict_slashes = False
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    print(app.url_map)
