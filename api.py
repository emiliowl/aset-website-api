# -*- coding: utf-8 -*-
from flask_cors import CORS
from apps.core.blueprints.therapists import bp as therapists_bp
from apps.core.blueprints.customers import bp as customers_bp
from apps.agenda.blueprints.agenda import bp as agenda_bp
from apps.agenda.blueprints.calendar import bp as calendar_bp
from apps.core.blueprints.mail_sender import bp as mailsender_bp


def configure_api(app):
    print('configuring blueprints...')
    app.register_blueprint(therapists_bp, url_prefix='/api/therapists')
    app.register_blueprint(customers_bp, url_prefix='/api/customers')
    app.register_blueprint(agenda_bp, url_prefix='/api/calendars/<string:name>/agendas')
    app.register_blueprint(calendar_bp, url_prefix='/api/calendars')
    app.register_blueprint(mailsender_bp, url_prefix='/api/sendmail')
    app.url_map.strict_slashes = False
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    print(app.url_map)
