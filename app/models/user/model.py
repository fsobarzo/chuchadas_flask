from flask.ext.sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from app.models.base_model import Model
from app import db

from datetime import datetime
import config


class User(Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    amount = db.Column(db.Integer)
    
    created_at = db.Column(db.DateTime(timezone=False))
    updated_at = db.Column(db.DateTime(timezone=False))

    def to_json(self):
        return {'username': self.username, 'amount': self.email, 'created_at': self.created_at, 'updated_at': self.updated_at}