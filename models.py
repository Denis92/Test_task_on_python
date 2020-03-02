from datetime import datetime

from pymongo import IndexModel, DESCENDING

from aiomongodel import Document, EmbeddedDocument
from aiomongodel.fields import (
    StrField, BoolField, ListField, EmbDocField, RefField, SynonymField,
    IntField, FloatField, DateTimeField, ObjectIdField)

class Mail(Document):
    _id = StrField(regex=r'[a-zA-Z0-9_]{3, 20}')
    send_status = StrField(required=True)
    date_time = DateTimeField(default=lambda: datetime.now())

    class Meta:
        collection = 'mail'