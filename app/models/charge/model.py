from flask.ext.sqlalchemy import SQLAlchemy
from app.models.base_model import Model
from app import db
from datetime import datetime

class Charge(Model):
	__tablename__ = 'charges'
	id          = db.Column(db.Integer, primary_key=True)
	topic       = db.Column(db.String(255))
	amout       = db.Column(db.Integer)
	by_user_id  = db.Column(db.Integer,db.ForeignKey('users.id'))
	created_at  = db.Column(db.DateTime(timezone=False),default=datetime.utcnow)

	by_user     = db.relationship('User',uselist=False,single_parent=True,foreign_keys = 'Charge.by_user_id')