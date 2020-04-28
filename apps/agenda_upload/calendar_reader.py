import os
from os.path import dirname
import csv
from apps.agenda.models import Agenda, Calendar, Therapist

def is_integer(n):
    try:
        int(n)
    except ValueError:
        return False
    else:
        return True


def process_agenda(file, calendar, therapist):
    file.save(os.path.join(dirname(__file__), file.filename))
    file_path = os.path.join(dirname(__file__), file.filename)
    created_agendas = []
    with open(file_path) as f:
        reader = csv.DictReader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            for k in row:
                if is_integer(row[k]):
                    print(f'Day: {k} -> Hour: {row[k]}')
                    agenda = Agenda()
                    agenda.date = f'{k}/05/2020'
                    agenda.time = f'{row[k]}:00'
                    agenda.calendar = calendar
                    agenda.therapist = therapist
                    created_agendas.append(agenda)

    return created_agendas

def process_agenda_mock(calendar, therapist):
    created_agendas = []
    with open('calendar_upload/template-agenda-aset.csv') as f:
        reader = csv.DictReader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        for row in reader:
            for k in row:
                if is_integer(row[k]):
                    print(f'Day: {k} -> Hour: {row[k]}')
                    agenda = Agenda()
                    agenda.date = f'{k}/05/2020'
                    agenda.time = f'{row[k]}:00'
                    agenda.calendar = calendar
                    agenda.therapist = therapist
                    created_agendas.append(agenda)

    return created_agendas
