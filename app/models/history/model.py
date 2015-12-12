from flask.ext.sqlalchemy import SQLAlchemy
from app.models.base_model import Model
from app import db
from datetime import datetime

class History(Model):
	__tablename__ = 'histories'
	id          = db.Column(db.Integer, primary_key=True)
	text        = db.Column(db.Text)
	tag         = db.Column(db.Integer)
	by_user_id  = db.Column(db.Integer,db.ForeignKey('users.id'))
	by_user     = db.relationship('User',uselist=False,single_parent=True,foreign_keys = 'History.by_user_id')
	created_at  = db.Column(db.DateTime(timezone=False),default=datetime.utcnow)