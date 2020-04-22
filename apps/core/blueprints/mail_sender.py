# -*- coding:utf-8 -*-
from datetime import datetime, timedelta
from flask import Blueprint, Response, abort, request

from infra.mail_sender import send_mail
from apps.agenda.models import Agenda, Appointment
from apps.core.models import Customer, Therapist

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

    send_mail('agendamento atendimento aset', agenda)
    return 'e-mail enviado com suscesso'