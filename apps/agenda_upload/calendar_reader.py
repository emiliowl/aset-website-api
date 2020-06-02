import os
from os.path import dirname
import csv
from apps.agenda.models import Agenda, Calendar, Therapist

def process_agenda(file, calendar, therapist, month, year):
    print('processing agenda...')
    file.save(os.path.join(dirname(__file__), file.filename))
    file_path = os.path.join(dirname(__file__), file.filename)
    print(f'file created: {file_path}')
    created_agendas = []
    with open(file_path) as f:
        reader = csv.DictReader(f, delimiter=';', quoting=csv.QUOTE_NONE)
        print('csv readed... starting to create agenda entries')
        rows = list(reader)
        print(f'number of rows: {len(rows)}')
        for row in rows:
            print(f'processing row {row}')
            for k in row:
                if row[k] is not None and row[k] != '':
                    print(f'Day: {k} -> Hour: {row[k]}')
                    agenda = Agenda()
                    agenda.date = f'{k}/{month}/{year}'
                    agenda.time = f'{row[k]}'
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
                if row[k] is not None and row[k] != '':
                    print(f'Day: {k} -> Hour: {row[k]}')
                    agenda = Agenda()
                    agenda.date = f'{k}/05/2020'
                    agenda.time = f'{row[k]}'
                    agenda.calendar = calendar
                    agenda.therapist = therapist
                    created_agendas.append(agenda)

    return created_agendas
