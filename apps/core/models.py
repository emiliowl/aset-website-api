from datetime import datetime
from mongoengine import (
    DateTimeField,
    EmailField,
    SortedListField,
    StringField
)

from apps.db import db
from apps.model_core import ModelCore


class Customer(db.Document, ModelCore):
    name = StringField(required=True, max_length=200)
    phone = StringField(required=True, max_length=20)
    email = EmailField(required=True, max_length=50, unique=True)
    last_modified = DateTimeField(default=datetime.now)

    def to_dict(self):
        serial = {}
        serial['name'] = self.name
        serial['phone'] = self.phone
        serial['email'] = self.email
        serial['last_modified'] = self.last_modified
        
        return serial


class Therapist(db.Document, ModelCore):
    name = StringField(required=True, max_length=200)
    slug = StringField(required=True, max_length=20)
    phone = StringField(required=True, max_length=20)
    email = EmailField(required=True, max_length=50, unique=True)
    specialties = SortedListField(field=StringField(max_length=20))
    last_modified = DateTimeField(default=datetime.now)

    def to_dict(self):
        serial = {}
        serial['name'] = self.name
        serial['slug'] = self.slug
        serial['phone'] = self.phone
        serial['email'] = self.email
        serial['last_modified'] = self.last_modified
        serial['specialties'] = self.specialties

        return serial
