# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from flask import Blueprint, Response, abort, request
from marshmallow import ValidationError

from infra.mail_sender import send_mail_sendgrid, send_contact_mail
from apps.agenda.models import Agenda, Appointment
from apps.core.models import Customer, Therapist
from apps.core.validations import CustomerSchema, MessageSchema

bp = Blueprint('mail_test', __name__)


@bp.route('/send', methods=["POST"])
def alive():
    customer = Customer()
    customer.email = 'emilio.murta@msitbrasil.com'
    customer.name = 'emilio murta resende'
    therapist = Therapist()
    therapist.email = 'silimatavares@gmail.com'
    therapist.name = 'Simone L. Tavares'
    agenda = Agenda()
    agenda.date = '21/04/2020'
    agenda.time = '23:00'
    agenda.therapist = therapist

    appointment = Appointment()
    appointment.customer = customer
    appointment.specialty = 'Especialidade teste'

    agenda.appointment = appointment

    send_mail_sendgrid('agendamento atendimento aset', agenda)
    return 'e-mail enviado com suscesso'

@bp.route('/contact', methods=["POST"])
def contact():
    contact_json = request.json
    try:
        customer = Customer(**CustomerSchema().load(contact_json['customer']))
        message_dict = MessageSchema().load(contact_json['message'])

        try:
            db_customer = Customer.objects.get(email=customer.email)
            db_customer.name = customer.name
            db_customer.phone = customer.phone
            customer = db_customer
            customer.save()
        except Exception as ex:
            print(f'customer not found {ex}, creating...')
            customer.save()
    
    except ValidationError as err:
        print('erro de validação!', err.messages)
        return err.messages, 400

    send_contact_mail(message_dict['subject'], message_dict['text'], customer)
    return 'e-mail enviado com suscesso'