from flask.ext.sqlalchemy import SQLAlchemy
from app.models.base_model import Model
from app import db
from datetime import datetime

class History(Model):
	MESSAGES = {
		CHUCHADA:   "%s dijo %i chuchada%s%s",
		EDIT:       "%s. Editado por %s",
		CHARGE:     "Carga final: %i, ingresado por %s",
		RESET:      "Chuchadas reseteadas",
		CHALLENGER: "Nuevo participante: %s",
		NEWVALUE:   "Nuevo valor por chuchada: %i, cambiado por: %s",
		CHARGEUSER: "Se cargan %i a %s, [%i] %s",
		FREE:       "%s obtiene %s gratis"
	}
	__tablename__ = 'histories'
	id          = db.Column(db.Integer, primary_key=True)
	text        = db.Column(db.Text)
	tag         = db.Column(db.Integer)
	by_user_id  = db.Column(db.Integer,db.ForeignKey('users.id'))
	by_user     = db.relationship('User',uselist=False,single_parent=True,foreign_keys = 'History.by_user_id')
	created_at  = db.Column(db.DateTime(timezone=False),default=datetime.utcnow)