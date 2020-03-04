import uuid
from datetime import datetime

from pymongo import IndexModel, DESCENDING

from aiomongodel import Document, EmbeddedDocument, fields
from aiomongodel.fields import (
    StrField, BoolField, ListField, EmbDocField, RefField, SynonymField,
    IntField, FloatField, DateTimeField, ObjectIdField)

class Mail(Document):
    _id = fields.StrField(default=lambda: str(uuid.uuid4()))
    send_status = StrField(required=True)
    date_time = DateTimeField(default=lambda: datetime.now())

    class Meta:
        collection = 'mail'