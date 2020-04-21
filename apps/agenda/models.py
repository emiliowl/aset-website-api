from datetime import datetime
from mongoengine import (
    DateTimeField,
    EmbeddedDocumentField,
    IntField,
    ReferenceField,
    StringField,
    SortedListField,
)

from apps.db import db
from apps.model_core import ModelCore
from apps.core.models import Customer, Therapist


class Appointment(db.EmbeddedDocument, ModelCore):
    customer = ReferenceField(Customer)
    specialty = StringField(required=True)

    def to_dict(self):
        serial = {}
        serial['specialty'] = self.specialty
        if(self.customer is not None):
            serial['customer'] = self.customer.to_dict()

        return serial


class Calendar(db.Document, ModelCore):
    name = StringField(required=True, unique=True)
    room_size = IntField(required=True)
    therapies = SortedListField(field=StringField(max_length=20))

    def to_dict(self):
        serial = {}
        serial['name'] = self.name
        serial['room_size'] = self.room_size
        serial['therapies'] = self.therapies

        return serial


class Agenda(db.Document, ModelCore):
    date = StringField(required=True)
    time = StringField(required=True, max_length=5)
    calendar = ReferenceField(Calendar, required=True)
    therapist = ReferenceField(Therapist, required=True)
    appointment = EmbeddedDocumentField(Appointment)
    last_modified = DateTimeField(default=datetime.now)

    def to_dict(self):
        serial = {}
        serial['date'] = self.date
        serial['time'] = self.time
        serial['last_modified'] = self.last_modified
        if(self.calendar is not None):
            serial['calendar'] = self.calendar.to_dict()
        if(self.therapist is not None):
            serial['therapist'] = self.therapist.to_dict()
        if(self.appointment is not None):
            serial['appointment'] = self.appointment.to_dict()

        return serial
