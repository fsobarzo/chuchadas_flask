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
	return create_history(HISTORY.CHUCHADA,message,user.id)

def edit_user(user,user_editor):
	message = HISTORY.MESSAGES[HISTORY.EDIT]
	message = message % (user.id,
	                     user.username.decode('utf8'),
	                     user.quantity,
	                     user.amount,
	                     user_editor.username.decode('utf8'))
	return create_history(HISTORY.EDIT,message,user.id)

def charge(charge,user):
	message = HISTORY.MESSAGES[HISTORY.CHARGE]
	message = message % (charge.amount, charge.topic.decode('utf8'), user.username.decode('utf8'))
	return create_history(HISTORY.CHARGE,message,user.id)

def charge_user(charge,user):
	message = HISTORY.MESSAGES[HISTORY.CHARGEUSER]
	message =  message % (user.amount, user.username.decode('utf8'), charge.id, charge.topic.decode('utf8'))
	return create_history(HISTORY.CHARGEUSER,message,user.id)

def new_challenger(user):
	message = HISTORY.MESSAGES[HISTORY.CHALLENGER]
	message = message % (user.username.decode('utf8'))
	return create_history(HISTORY.CHALLENGER,message,user.id)

def create_history(tag,message,user_id):
	history = History()
	history.tag        = tag
	history.text       = message
	history.by_user_id = user_id
	history.created_at = datetime.now()
	
	db.session.add(history)
	db.session.commit()
	return history