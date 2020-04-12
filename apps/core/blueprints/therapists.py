# -*- coding:utf-8 -*-
import json
from flask import Blueprint, Response, abort, request

from apps.core.models import Therapist
from apps.serializer import default

bp = Blueprint('therapists', __name__)


@bp.route('/healthcheck')
def alive():
    return 'therapists stil breathing...'


@bp.route('/')
def get_all():
    try:
        therapists = Therapist.objects
        print(therapists)

        therapists_json = json.dumps(
            [t.to_dict() for t in therapists],
            default=default)

        return Response(
            therapists_json,
            mimetype='application/json',
            status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:email>')
def get(email):
    try:
        therapist = Therapist.objects.get(email=email)
        therapist_json = json.dumps(therapist.to_dict(), default=default)
        return Response(
            therapist_json, 
            mimetype='application/json', 
            status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/', methods=["POST"])
def create():
    try:
        therapist_json = request.json
        therapist = Therapist(**therapist_json)
        therapist.save()

        return Response(status=201)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:email>', methods=["PUT"])
def update(email):
    try:
        therapist_json = request.json
        therapist = Therapist.objects.get(email=email)

        therapist.update_values(therapist_json)
        therapist.save()

        return Response(status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:email>', methods=["DELETE"])
def remove(email):
    try:
        therapist = Therapist.objects.get(email=email)

        therapist.delete()

        therapist_json = json.dumps(therapist.to_dict(), default=default)
        return Response(
            therapist_json,
            mimetype='application/json',
            status=200)
    except Exception as ex:
        print(ex)
        abort(500)
