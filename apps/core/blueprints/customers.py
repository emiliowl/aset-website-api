# -*- coding:utf-8 -*-
import json
from flask import Blueprint, Response, abort, request

from apps.core.models import Customer
from apps.serializer import default

bp = Blueprint('customers', __name__)


@bp.route('/healthcheck')
def alive():
    return 'customers stil breathing...'


@bp.route('/')
def get_all():
    try:
        customers = Customer.objects
        print(customers)

        customers_json = json.dumps(
            [t.to_dict() for t in customers],
            default=default)

        return Response(
            customers_json,
            mimetype='application/json',
            status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:email>')
def get(email):
    try:
        customer = Customer.objects.get(email=email)
        customer_json = json.dumps(customer.to_dict(), default=default)
        return Response(customer_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/', methods=["POST"])
def create():
    try:
        customer_json = request.json
        customer = Customer(**customer_json)
        customer.save()

        return Response(status=201)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:email>', methods=["PUT"])
def update(email):
    try:
        customer_json = request.json
        customer = Customer.objects.get(email=email)

        customer.update_values(customer_json)
        customer.save()

        return Response(status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:email>', methods=["DELETE"])
def remove(email):
    try:
        customer = Customer.objects.get(email=email)

        customer.delete()

        customer_json = json.dumps(customer.to_dict(), default=default)
        return Response(customer_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)
