from flask import Blueprint, request, jsonify, request
from sqlalchemy import exc
from app import app, db
from app import auto
from app.modules import history_module
from app.models.user.model import User
from app.models.history.model import History
from app.models.charge.model import Charge
from app.models.user import constants as USER
from app.models.charge import constants as CHARGE
from datetime import datetime

mod_core = Blueprint('welcome',__name__)

#METHODS: GET
#DESCRIPTION: WELCOME
@mod_core.route("/", methods = ['GET'])
def welcome():
	return (jsonify({'welcome': 'Connect to api successfully'}), 200)

#METHODS: GET
#DESCRIPTION: RUTAS
@mod_core.route("/routes", methods =['GET'])
def routes():
	func_list = {}
	for rule in app.url_map.iter_rules():
		if rule.endpoint != 'static':
			func_list[rule.rule] = rule.methods

	return (jsonify(func_list), 200)

@mod_core.route("/documentation")
def documentation():
	return auto.html()

#METHODS: GET
#DESCRIPTION: LISTA USUARIOS
@mod_core.route("/users", methods=['GET'])
def show_users():
	users = User.query.all()
	users_dict = []
	for user in users:
		users_dict.append(user.to_dict(show_all=True))
	return (jsonify({'users': users_dict}),200)

#METHODS: POST 
#DESCRIPTION: NUEVO USUARIO
@mod_core.route("/users", methods=['POST'])
def add_chucha():
	if not request.json:
		return (jsonify({"error":"Data no enviada"}),400)
	if USER.USERNAME not in request.json:
		return (jsonify({"error":"Faltan datos"}),400)

	user = User()
	user.username = request.json[USER.USERNAME]
	try:
		db.session.add(user)
		db.session.commit()
	except exc.IntegrityError as e:
		message = "Usuario %s ya existe" % (user.username)
		return (jsonify({"error":message}),400)
	
	history = history_module.new_challenger(user)

	response = {}
	response['user'] = user.to_dict(show_all=True)
	response['message'] = history.to_dict(show_all=True,hide=['by_user','by_user_id'])
	return (jsonify(response),201)

#METHODS: PUT
#DESCRIPTION: NUEVA CHUCHADA
@mod_core.route("/users/<path:player>/chuchada", methods=['GET','POST','PUT'])
def update_player(player):
	user = User.query.filter_by(username=player).first()
	if not user:
		return (jsonify({"error":"Usuario no existe"}),400)

	quantity = 1
	if request.json and "quantity" in request.json:
		quantity = int(request.json["quantity"])
		if quantity < 0:
			return (jsonify({"error":"Cantidad menor a 1"}),400)

	user.quantity+= quantity
	user.amount+= quantity*USER.VALUE
	user.quantity_total+=quantity
	user.amount_total+= quantity*USER.VALUE
	user.updated_at = datetime.now()
	db.session.commit()
	
	history = history_module.new_chuchada(user,quantity)
	
	response = {}
	response['user'] = user.to_dict(show_all=True)
	response['message'] = history.to_dict(show_all=True,hide=['by_user','by_user_id'])
	return (jsonify(response),200)

#METHODS: PUT
#DESCRIPTION: EDITAR USUARIO
@mod_core.route("/users/<int:user_id>",methods=["PUT"])
def update_user(user_id):
	user = User.query.get(user_id)
	if not user:
		return (jsonify({"error":"Usuario no existe"}),400)
	
	if not request.json:
		return (jsonify({"error":"Data no enviada"}),400)
	
	if not USER.EDITOR in request.json:
		return (jsonify({"error":"Falta usuario responsable"}))
	
	user_editor_id = int(request.json[USER.EDITOR])
	user_editor = User.query.get(user_editor_id)
	if not user_editor:
		return (jsonify({"error":"Usuario editor no existe"}),400)
	
	params = user.to_dict(show_all=True,hide=["created_at","updated_at"])
	for key in USER.COLUMNS:
		if key in request.json:
			params[key] = request.json[key]

	if params[USER.QUANTITY] < 0:
		return (jsonify({"error":"Cantidad no puede tener valores negativos"}),400)
	elif params[USER.QUANTITY] ==  user.quantity:
		return (jsonify({"error":"Usuario ya registra la cantidad de chuchadas"}),400)

	old_quantity    = user.quantity
	user.username   = params[USER.USERNAME]
	user.quantity   = params[USER.QUANTITY]
	user.amount     = params[USER.QUANTITY]*USER.VALUE
	if old_quantity == 0:
		user.quantity_total+= params[USER.QUANTITY] 
		user.amount_total+= params[USER.QUANTITY]*USER.VALUE
	elif old_quantity > params[USER.QUANTITY]:
		user.quantity_total-= old_quantity - params[USER.QUANTITY]
		user.amount_total-= (old_quantity - params[USER.QUANTITY])*USER.VALUE
	elif old_quantity < params[USER.QUANTITY]:
		user.quantity_total+= params[USER.QUANTITY] - old_quantity
		user.amount_total+= (params[USER.QUANTITY] - old_quantity)*USER.VALUE

	user.updated_at = datetime.now()
	db.session.commit()

<<<<<<< HEAD
	return (jsonify({"user":user.to_dict(show_all=True)}),200)
=======
	history = history_module.edit_user(user,user_editor)
	
	response = {}
	response['user'] = user.to_dict(show_all=True)
	response['message'] = history.to_dict(show_all=True,hide=['by_user','by_user_id'])

	return (jsonify(response),200)

#METHODS: GET
#DESCRIPTION: HISTORIA
#TODO: CARGAR ANTERIORES
@mod_core.route("/histories",methods=["GET"])
@mod_core.route('/histories/',methods=["GET"])
@mod_core.route('/histories/<int:user_id>',methods=["GET"])
def get_histories(user_id=None):
	if user_id is None:
		histories = History.query.limit(15).all()
	else:
		histories = History.query.filter(History.by_user_id == user_id).limit(15).all()

	histories_dict = []
	for history in histories:
		histories_dict.append(history.to_dict(show_all=True))
	return (jsonify({'histories': histories_dict}),200)

#METHODS: GET
#DESCRIPTION: LISTAR CARGOS 
@mod_core.route("/charges",methods=["GET"])
def charges():
	charges = Charge.query.limit(15).all()
	charges_dict = []
	for charge in charges:
		charges_dict.append(charge.to_dict(show_all=True))
	return (jsonify({'charges': charges_dict}),200)

#METHODS: POST
#DESCRIPTION: NUEVO CARGO
@mod_core.route("/charge",methods=["POST"])
def charge():
	if not request.json:
		return (jsonify({"error":"Data no enviada"}),400)
	
	params = {}
	for key in CHARGE.COLUMNS:
		if key in request.json:
			params[key] = request.json[key]
		else:
			return (jsonify({"error":"Falta usuario responsable"}),400)

	user_id = int(params[CHARGE.BY_USER])
	user = User.query.get(user_id)
	if not user:
		return (jsonify({"error":"Usuario no existe"}),400)

	users = User.query.all()
	final_amount = 0
	for u in users:
		final_amount+= u.amount

	if final_amount == 0:
		return (jsonify({"error":"Monto Final: 0"}),400)
	charge = Charge()
	charge.amount     = final_amount
	charge.topic      = params[CHARGE.TOPIC]
	charge.by_user_id = params[CHARGE.BY_USER]
	charge.created_at = datetime.now()

	db.session.add(charge)
	db.session.commit()

	history = history_module.charge(charge,user)
	
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
>>>>>>> master
