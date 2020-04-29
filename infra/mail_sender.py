import yagmail
import os
from ics import Calendar, Event
from datetime import timedelta, datetime

from apps.agenda.models import Agenda, Customer

def send_contact_mail(subject, text, customer: Customer):
    curdir = os.getcwd()
    with open(f'{curdir}{os.sep}apps{os.sep}core{os.sep}email_templates{os.sep}contact.html') as templ:
        body = ''.join(templ.readlines())
        body = body.replace('{{name}}', customer.name)
        body = body.replace('{{email}}', customer.email)
        body = body.replace('{{phone}}', customer.phone)
        body = body.replace('{{date}}', datetime.now().strftime('%d/%m/%Y'))
        body = body.replace('{{text}}', text)

        yag = yagmail.SMTP(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PWD"))
        yag.send(
            to=os.getenv("EMAIL_SENDER"),
            subject=subject,
            contents=body
        )

def send_mail(description, agenda: Agenda):
    c = Calendar()
    e = Event()
    e.name = 'Atendimento Aset Terapias'

    str_begin = '-'.join(reversed(agenda.date.split('/')))
    str_begin = f'{str_begin} {agenda.time}'
    e.begin = (datetime.strptime(str_begin, '%Y-%m-%d %H:%M') + timedelta(hours=3))
    e.end = (datetime.strptime(str_begin, '%Y-%m-%d %H:%M') + timedelta(hours=4))

    e.attendees=[agenda.appointment.customer.email, agenda.therapist.email]
    e.description = description
    c.events.add(e)

    curdir = os.getcwd()

    with open(f'{curdir}{os.sep}go.ics', 'w') as f:
        f.writelines(c)

    with open(f'{curdir}{os.sep}apps{os.sep}agenda{os.sep}email_templates{os.sep}appointment-confirmation.html') as templ:
        body = ''.join(templ.readlines())
        body = body.replace('{{nome}}', agenda.appointment.customer.name)
        body = body.replace('{{nome_terapia}}', agenda.appointment.specialty)
        body = body.replace('{{nome_terapeuta}}', agenda.therapist.name)
        body = body.replace('{{data}}', agenda.date)
        body = body.replace('{{hora}}', agenda.time)

        body = body.replace('{{api}}', os.getenv("API_ENDPOINT"))
        body = body.replace('{{calendar}}', agenda.calendar.name)
        body = body.replace('{{therapist_mail}}', agenda.therapist.email)
        body = body.replace('{{date}}', agenda.date.replace('/', '-'))
        body = body.replace('{{hour}}', agenda.time)

        yag = yagmail.SMTP(os.getenv("EMAIL_SENDER"), os.getenv("EMAIL_PWD"))
        yag.send(
            to=agenda.appointment.customer.email,
            bcc=agenda.therapist.email,
            subject="Aset Terapias : Confirmação de consulta",
            contents=body,
            attachments=[f'{curdir}{os.sep}go.ics']
        )