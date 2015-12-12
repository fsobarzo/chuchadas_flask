from app.models.history.model import History
from app.models.history import constants as HISTORY
from app import db
from datetime import datetime
import random

def new_chuchada(user,quantity):
	message = HISTORY.MESSAGES[HISTORY.CHUCHADA]
	pool_message = random.choice(HISTORY.POOL)
	is_plural = "s" if quantity >= 2 else ""
	message = message % (user.username, quantity, is_plural, pool_message.decode('utf8'))
	history = History()
	history.tag        = HISTORY.CHUCHADA
	history.text       = message
	history.by_user_id = user.id
	history.created_at = datetime.now()
	
	db.session.add(history)
	db.session.commit()
	return history

def edit_user(user,user_editor):
	message = HISTORY.MESSAGES[HISTORY.EDIT]
	message_edit = "User: %i, Nombre: %s, Cantidad: %i, Dinero: %i" % (user.id, user.username, user.quantity,user.amount)
	message = message % (message_edit.decode('utf8'),user.username.decode('utf8'))
	history = History()
	history.tag        = HISTORY.EDIT
	history.text       = message
	history.by_user_id = user_editor.id
	history.created_at = datetime.now()
	
	db.session.add(history)
	db.session.commit()
	return history

def charge(charge,user):
	message = HISTORY.MESSAGES[HISTORY.CHARGE]
	message = message % (charge.amount, user.username.decode('utf8'))
	history = History()
	history.tag        = HISTORY.CHARGE
	history.text       = message
	history.by_user_id = user.id
	history.created_at = datetime.now()
	
	db.session.add(history)
	db.session.commit()
	return history

def charge_user(charge,user):
	message = HISTORY.MESSAGES[HISTORY.CHARGEUSER]
	message =  message % (user.amount, user.username.decode('utf8'), charge.id, charge.topic.decode('utf8'))
	history = History()
	history.tag        = HISTORY.CHARGEUSER
	history.text       = message
	history.by_user_id = user.id
	history.created_at = datetime.now()

	db.session.add(history)
	db.session.commit()
	return history

def new_challenger(user):
	message = HISTORY.MESSAGES[HISTORY.CHALLENGER]
	message = message % (user.username.decode('utf8'))
	history = History()
	history.tag        = HISTORY.CHALLENGER
	history.text       = message
	history.by_user_id = user.id
	history.created_at = datetime.now()
	
	db.session.add(history)
	db.session.commit()
	return history