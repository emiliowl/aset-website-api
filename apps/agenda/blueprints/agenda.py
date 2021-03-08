# -*- coding:utf-8 -*-
import json
import pytz
from datetime import datetime

from flask import Blueprint, Response, abort, request
from mongoengine import Q
from marshmallow import ValidationError

from apps.agenda.models import Agenda, Appointment, Calendar
from apps.core.models import Therapist, Customer
from apps.core.validations import CustomerSchema
from apps.serializer import default
from infra.mail_sender import send_mail_sendgrid, send_cancel_mail_sendgrid

from apps.agenda_upload.calendar_reader import process_agenda

bp = Blueprint('agenda', __name__)


@bp.route('/healthcheck')
def alive():
    return 'agenda stil breathing...'


@bp.route('/')
def get_all(name):
    try:
        calendar = Calendar.objects.get(name=name)
        agendas = Agenda.objects(calendar=calendar)
        print(agendas)
        agendas_json = json.dumps(
            [t.to_dict() for t in agendas],
            default=default)
        return Response(agendas_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/next-dates')
def get_next_dates(name):
    try:
        calendar = Calendar.objects.get(name=name)
        agendas = Agenda.objects(calendar=calendar, appointment=None)
        print(agendas)
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz)
        today = now.date()
        current_hour = f'{str(now.hour).zfill(2)}:00'
        agendas = [
            ag.date for ag
            in agendas
            if Agenda.objects(
                calendar=calendar,
                date=ag.date,
                time=ag.time,
                appointment__exists=True)
            .count() < int(calendar.room_size)
            and (
                datetime.strptime(ag.date, '%d/%m/%Y').date() > today
            )
            or (
                datetime.strptime(ag.date, '%d/%m/%Y').date() == today
                and ag.time > current_hour
            )
        ]
        all_dates_list = [
            datetime.strptime(ag, '%d/%m/%Y').date()
            for ag in list(agendas)
        ]

        all_dates_list.sort()
        dates_list = [
            dt for dt in list(dict.fromkeys(all_dates_list))
        ]

        next_dates_sorted = dates_list[:30]

        dates_json = json.dumps(next_dates_sorted, default=default)
        return Response(dates_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/next-dates/<string:specialty>')
def get_next_dates_for_specialty(name, specialty):
    try:
        calendar = Calendar.objects.get(name=name)
        therapists = Therapist.objects(Q(specialties__contains=specialty))
        print(therapists)
        agendas = Agenda.objects(
                Q(
                    calendar=calendar,
                    appointment=None,
                    therapist__in=therapists
                ),
            )
        print(agendas)
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz)
        today = now.date()
        current_hour = f'{str(now.hour).zfill(2)}:00'
        agendas = [
            ag.date for ag in list(agendas)
            if Agenda.objects(
                calendar=calendar,
                date=ag.date,
                time=ag.time,
                appointment__exists=True
            ).count() < int(calendar.room_size)
            and (
                datetime.strptime(ag.date, '%d/%m/%Y').date() > today
            )
            or (
                datetime.strptime(ag.date, '%d/%m/%Y').date() == today
                and ag.time > current_hour
            )
        ]

        all_dates_list = [
            datetime.strptime(dt, '%d/%m/%Y').date() for dt in list(agendas)
        ]
        all_dates_list.sort()
        dates_list = [dt for dt in list(dict.fromkeys(all_dates_list))]

        next_dates_sorted = dates_list[:30]

        dates_json = json.dumps(next_dates_sorted, default=default)
        return Response(dates_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('for-date/<string:agenda_date>', methods=["GET"])
def get_for_date(name, agenda_date):
    try:
        calendar = Calendar.objects.get(name=name)
        agendas = Agenda.objects(
            calendar=calendar,
            date=agenda_date.replace('-', '/'),
            appointment=None)
        print(agendas)
        tz = pytz.timezone('America/Sao_Paulo')
        now = datetime.now(tz)
        today = now.date()
        current_hour = f'{str(now.hour).zfill(2)}:00'
        agendas = [
            ag for ag in agendas
            if Agenda.objects(
                calendar=calendar,
                date=ag.date,
                time=ag.time,
                appointment__exists=True
            ).count() < int(calendar.room_size)
            and (
                datetime.strptime(ag.date, '%d/%m/%Y').date() > today
            )
            or (
                datetime.strptime(ag.date, '%d/%m/%Y').date() == today
                and ag.time > current_hour
            )
        ]

        agendas_json = json.dumps(
            [t.to_dict() for t in agendas],
            default=default)
        return Response(
            agendas_json,
            mimetype='application/json',
            status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('for-date/<string:agenda_date>/<string:specialty>', methods=["GET"])
def get_for_date_and_specialty(name, agenda_date, specialty):
    try:
        calendar = Calendar.objects.get(name=name)
        therapists = Therapist.objects(Q(specialties__contains=specialty))
        print(therapists)
        agendas = Agenda.objects(
            Q(
                calendar=calendar,
                appointment=None,
                date=agenda_date.replace('-', '/'),
                therapist__in=therapists
            )
        )
        print(agendas)
        agendas = [ag for ag in agendas if Agenda.objects(calendar=calendar, date=ag.date, time=ag.time, appointment__exists=True).count() < int(calendar.room_size)]

        agendas_json = json.dumps(
            [t.to_dict() for t in agendas],
            default=default)
        return Response(
            agendas_json,
            mimetype='application/json',
            status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/<string:therapist_email>')
def get(name, therapist_email):
    try:
        calendar = Calendar.objects.get(name=name)
        therapist = Therapist.objects.get(email=therapist_email)
        agendas = Agenda.objects(calendar=calendar, therapist=therapist)
        print(agendas)
        agendas_json = json.dumps(
            [t.to_dict() for t in agendas],
            default=default)
        return Response(agendas_json, mimetype='application/json', status=200)
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/', methods=["POST"])
def create(name):
    try:
        agenda_json = request.json
        agenda = Agenda(**agenda_json)
        calendar = Calendar.objects().get(name=name)
        agenda.calendar = calendar
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
    '/cancel/<string:therapist_email>/<string:agenda_date>/<string:agenda_time>',
    methods=["GET"])
def remove_from_email(name, therapist_email, agenda_date, agenda_time):
    try:
        calendar = Calendar.objects.get(name=name)
        therapist = Therapist.objects.get(email=therapist_email)
        agenda: Agenda = Agenda.objects.get(
            calendar=calendar,
            therapist=therapist,
            date=agenda_date.replace('-', '/'),
            time=agenda_time)

        date_str = f"{agenda_date.replace('-', '/')} {agenda_time.split(':')[0]}:{agenda_time.split(':')[1]}"
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        date_diff = date - datetime.now()
        hours = date_diff.total_seconds() / 60 / 60
        print('Diferença de horas:')
        print(hours)

        # send e-mail related to appointment
        send_cancel_mail_sendgrid(agenda)

        agenda.appointment = None
        agenda.save()

        return 'Cancelamento realizado com sucesso.', 200
    except Exception as ex:
        print(ex)
        abort(500)


@bp.route(
    '/<string:therapist_email>/<string:agenda_date>/<string:agenda_time>',
    methods=["DELETE"])
def remove(name, therapist_email, agenda_date, agenda_time):
    try:
        calendar = Calendar.objects.get(name=name)
        therapist = Therapist.objects.get(email=therapist_email)
        agenda = Agenda.objects.get(
            calendar=calendar,
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
def book(name, therapist_email, agenda_date, agenda_time):
    try:
        calendar = Calendar.objects.get(name=name)
        therapist = Therapist.objects.get(email=therapist_email)
        agenda = Agenda.objects.get(
            calendar=calendar,
            therapist=therapist,
            date=agenda_date.replace('-', '/'),
            time=agenda_time)

        appointment_json = request.json

        customer = Customer(**CustomerSchema().load(appointment_json['customer']))

        try:
            db_customer = Customer.objects.get(email=customer.email)
            db_customer.name = customer.name
            db_customer.phone = customer.phone
            customer = db_customer
            customer.save()
        except Exception as ex:
            print(f'customer not found {ex}')
            customer.save()

        appointment = Appointment()
        appointment.customer = customer
        appointment.specialty = appointment_json['specialty']
        appointment.text = appointment_json['text']

        agenda.appointment = appointment
        agenda.save()

        # send e-mail related to appointment
        send_mail_sendgrid('agendamento atendimento aset', agenda)

        agenda_json = json.dumps(agenda.to_dict(), default=default)
        return Response(agenda_json, mimetype='application/json', status=200)
    except ValidationError as err:
        print('erro de validação!', err.messages)
        return err.messages, 400

    except Exception as ex:
        print(ex)
        abort(500)


@bp.route('/upload/<string:therapist_email>/<string:month>/<string:year>',
          methods=["POST"])
def upload(name, therapist_email, month, year):
    # check if the post request has the file part
    if 'file' not in request.files:
        return 'Please upload a file', 400
    file = request.files['file']
    if file.filename == '':
        return 'Please upload a file... this is empty', 400

    print('processing upload...')

    calendar = Calendar.objects.get(name=name)
    therapist = Therapist.objects.get(email=therapist_email)
    agenda_list = Agenda.objects(
            calendar=calendar,
            therapist=therapist,
            date__contains=f'{month}/{year}',
            appointment=None)
    print(agenda_list)
    print(f'removing agenda entries {len(agenda_list)}')
    for agenda in agenda_list:
        agenda.delete()

    agendas = process_agenda(file, calendar, therapist, month, year)
    agenda_list_booked = Agenda.objects(
            calendar=calendar,
            therapist=therapist,
            date__contains=f'{month}/{year}',
            appointment__exists=True)
    print('all booked agendas')
    print(agenda_list_booked)
    agendas_to_persist = list(filter(lambda a: len(
        list(filter(lambda b: b.calendar.name == a.calendar.name
                           and b.therapist.name == a.therapist.name
                           and b.date == a.date
                           and b.time == a.time,
                           agenda_list_booked))
        ) == 0, agendas))

    print(f'persisting agendas : {list(agendas_to_persist)}')
    for agenda in agendas_to_persist:
        print(f'saving agenda {agenda.date} {agenda.time}')
        agenda.save()

    return 'processamento efetuado com sucesso!', 200
