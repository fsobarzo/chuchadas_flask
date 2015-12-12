from flask.ext.sqlalchemy import SQLAlchemy
from app.models.base_model import Model
from app import db
from datetime import datetime

class User(Model):
	__tablename__ = 'users'
	id       = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	quantity = db.Column(db.Integer,default=0)
	amount   = db.Column(db.Integer,default=0)
	quantity_total = db.Column(db.Integer,default=0)
	amount_total   = db.Column(db.Integer,default=0)
	
	created_at = db.Column(db.DateTime(timezone=False),default=datetime.utcnow)
	updated_at = db.Column(db.DateTime(timezone=False),default=datetime.utcnow)