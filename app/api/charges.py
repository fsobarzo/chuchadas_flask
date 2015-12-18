from flask import Blueprint, request, jsonify, request

from app.models.user.model import User
from app.models.charge.model import Charge
from app.models.charge import constants as CHARGE
from app.modules import history_module

from datetime import datetime
from app import db, errors

mod_charges = Blueprint('charges',__name__)

#ADD PAGINATION

#METHODS: GET
#DESCRIPTION: LISTAR CARGOS 
@mod_charges.route("/charges/",methods=["GET"])
def charges():
	charges = Charge.query.limit(15).all()
	return (jsonify({'charges': [charge.to_dict(show_all=True) for charge in charges] }),200)

#METHODS: POST
#DESCRIPTION: NUEVO CARGO
@mod_charges.route("/charge",methods=["POST"])
def charge():
	if not request.json:
		raise errors.InvalidData()
	
	params = {}
	for key in CHARGE.COLUMNS:
		if key in request.json:
			params[key] = request.json[key]
		else:
			msg = 'Missing parameter: {column}'.format(column=key)
			raise errors.InvalidData(msg) 

	user_id = int(params[CHARGE.BY_USER])
	user = User.query.get_or_404(user_id)

	final_amount = sum(u.amount for u in User.query.all())
	if final_amount == 0:
		return (jsonify({"error":"Monto Final: 0"}),400)
	
	charge = Charge()
	charge.amount     = final_amount
	charge.topic      = params[CHARGE.TOPIC]
	charge.by_user_id = user.id
	charge.created_at = datetime.now()

	db.session.add(charge)
	db.session.commit()
	history = history_module.charge(charge,user)

	# ENVIAR A OTRA FUNCION
	users = User.query.all()
	for u in users:
		history_module.charge_user(charge,u)
		u.amount = 0
		u.quantity = 0
		u.updated_at = datetime.now()
	db.session.commit()
	
	response = {}
	response['user'] = user.to_dict(show_all=True)
	response['charge'] = charge.to_dict(show_all=True,hide=['by_user'])
	response['message'] = history.to_dict(show_all=True,hide=['by_user'])
	return (jsonify(response),200)