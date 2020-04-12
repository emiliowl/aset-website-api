# -*- coding:utf-8 -*-
import json
from datetime import datetime, date

from flask import Blueprint, Response, abort, request
from mongoengine import Q

from apps.agenda.models import Agenda, Appointment
from apps.core.models import Therapist, Customer
from apps.serializer import default

bp = Blueprint('agenda', __name__)


@bp.route('/healthcheck')
def alive():
    return 'agenda stil breathing...'


@bp.route('/')
def get_all():
    try:
        agendas = Agenda.objects
        print(agendas)
        agendas_json = json.dumps(
            [t.to_dict() for t in agendas],
            default=default)
        return Response(agendas_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/next-dates')
def get_next_dates():
    try:
        agendas = Agenda.objects(appointment=None).distinct(field="date")

        all_dates_list = [
            datetime.strptime(dt, '%d/%m/%Y').date() for dt in list(agendas)
        ]
        all_dates_list.sort(reverse=True)
        dates_list = [dt for dt in all_dates_list if dt >= date.today()]

        next_dates_sorted = dates_list[:9]

        dates_json = json.dumps(next_dates_sorted, default=default)
        return Response(dates_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/next-dates/<string:specialty>')
def get_next_dates_for_specialty(specialty):
    try:
        therapists = Therapist.objects(Q(specialties__contains=specialty))
        print(therapists)
        agendas = Agenda.objects(
                Q(appointment=None, therapist__in=therapists),
            )\
            .distinct(field="date")

        all_dates_list = [
            datetime.strptime(dt, '%d/%m/%Y').date() for dt in list(agendas)
        ]
        all_dates_list.sort(reverse=True)
        dates_list = [dt for dt in all_dates_list if dt >= date.today()]

        next_dates_sorted = dates_list[:9]

        dates_json = json.dumps(next_dates_sorted, default=default)
        return Response(dates_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('for-date/<string:agenda_date>', methods=["GET"])
def get_for_date(agenda_date):
    try:
        agendas = Agenda.objects(date=agenda_date.replace('-', '/'))
        print(agendas)
        agendas_json = json.dumps(
            [t.to_dict() for t in agendas if t.appointment is None],
            default=default)
        return Response(
            agendas_json,
            mimetype='application/json',
            status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('for-date/<string:agenda_date>/<string:specialty>', methods=["GET"])
def get_for_date_and_specialty(agenda_date, specialty):
    try:
        therapists = Therapist.objects(Q(specialties__contains=specialty))
        print(therapists)
        agendas = Agenda.objects(
            Q(
                appointment=None,
                date=agenda_date.replace('-', '/'),
                therapist__in=therapists
            )
        )
        print(agendas)

        agendas_json = json.dumps(
            [t.to_dict() for t in agendas if t.appointment is None],
            default=default)
        return Response(
            agendas_json,
            mimetype='application/json',
            status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:therapist_email>')
def get(therapist_email):
    try:
        therapist = Therapist.objects.get(email=therapist_email)
        agendas = Agenda.objects(therapist=therapist)
        print(agendas)
        agendas_json = json.dumps(
            [t.to_dict() for t in agendas],
            default=default)
        return Response(agendas_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/', methods=["POST"])
def create():
    try:
        agenda_json = request.json
        agenda = Agenda(**agenda_json)
        therapist = Therapist\
            .objects\
            .get(email=agenda_json['therapist']['email'])
        agenda.therapist = therapist
        agenda.save()

        return Response(status=201)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route(
    '/<string:therapist_email>/<string:agenda_date>/<string:agenda_time>',
    methods=["DELETE"])
def remove(therapist_email, agenda_date, agenda_time):
    try:
        therapist = Therapist.objects.get(email=therapist_email)
        agenda = Agenda.objects.get(
            therapist=therapist,
            date=agenda_date.replace('-', '/'),
            time=agenda_time)

        agenda.delete()

        agenda_json = json.dumps(agenda.to_dict(), default=default)
        return Response(agenda_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route(
    '/<string:therapist_email>/<string:agenda_date>/<string:agenda_time>',
    methods=["POST"])
def book(therapist_email, agenda_date, agenda_time):
    try:
        therapist = Therapist.objects.get(email=therapist_email)
        print(therapist.email)
        print(agenda_date)
        print(agenda_time)
        agenda = Agenda.objects.get(
            therapist=therapist,
            date=agenda_date.replace('-', '/'),
            time=agenda_time)

        appointment_json = request.json
        print(appointment_json)
        customer = Customer(**appointment_json['customer'])

        try:
            lookup_customer = Customer.objects.get(email=customer.email)
            customer = lookup_customer
        except Exception as ex:
            print(f'customer not found {ex}')
            customer.save()

        appointment = Appointment()
        appointment.customer = customer
        appointment.specialty = appointment_json['specialty']

        agenda.appointment = appointment
        agenda.save()

        agenda_json = json.dumps(agenda.to_dict(), default=default)
        return Response(agenda_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)
