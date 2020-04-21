# -*- coding:utf-8 -*-
import json

from flask import Blueprint, Response, abort, request
from mongoengine import Q

from apps.agenda.models import Calendar
from apps.serializer import default


bp = Blueprint('calendar', __name__)


@bp.route('/healthcheck')
def alive():
    return 'calendar stil breathing...'


@bp.route('/')
def get_all():
    try:
        calendars = Calendar.objects()
        print(calendars)
        calendars_json = json.dumps(
            [t.to_dict() for t in calendars],
            default=default)
        return Response(calendars_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:name>')
def get(name):
    try:
        calendar = Calendar.objects.get(name=name)
        calendar_json = json.dumps(calendar.to_dict(), default=default)

        return Response(calendar_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/', methods=["POST"])
def create():
    try:
        calendar_json = request.json
        calendar = Calendar(**calendar_json)
        calendar.save()

        return Response(status=201)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:name>', methods=["DELETE"])
def remove(name):
    try:
        calendar = Calendar.objects.get(name=name)
        calendar.delete()

        calendar_json = json.dumps(calendar.to_dict(), default=default)
        return Response(calendar_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)
        