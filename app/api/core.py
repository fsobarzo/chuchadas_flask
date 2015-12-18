from flask import Blueprint, request, jsonify, request
from sqlalchemy import exc
from app import app, db, errors
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
@mod_core.route("/routes/", methods =['GET'])
def routes():
	func_list = {}
	for rule in app.url_map.iter_rules():
		if rule.endpoint != 'static':
			func_list[rule.rule] = rule.methods

	return (jsonify(func_list), 200)

@mod_core.route("/documentation")
def documentation():
	return auto.html(groups=['public','private'])

#METHODS: GET
#DESCRIPTION: LISTA USUARIOS
@mod_core.route("/users/", methods=['GET'])
@auto.doc(groups=['public'])
def show_users():
	"""Muestra a los usuarios."""
	users = User.query.all()
	return (jsonify({'users': [user.to_dict(show_all=True) for user in users] }),200)

#METHODS: GET
#DESCRIPTION: INFO USUARIO
@mod_core.route("/users/<int:user_id>",methods=['GET'])
@auto.doc(groups=['private'])
def get_user(user_id):
	"""Muestra un usuario."""
	user =  User.query.get_or_404(user_id)
	return (jsonify({'user': user.to_dict(show_all=True)}))

#METHODS: POST 
#DESCRIPTION: NUEVO USUARIO
@mod_core.route("/users/", methods=['POST'])
def add_chucha():
	if not request.json:
		raise errors.InvalidData()
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
@mod_core.route("/users/<player>/chuchada", methods=['GET','POST','PUT'])
def update_player(player):
	user = User.query.filter_by(username=player).first_or_404()
	
	if request.json and "quantity" in request.json:
		quantity = int(request.json["quantity"])
		if quantity < 0:
			return (jsonify({"error":"Cantidad menor a 1"}),400)
	else:
		quantity = 1

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
	user = User.query.get_or_404(user_id)
	if not request.json:
		raise errors.InvalidData()
	
	if not USER.EDITOR in request.json:
		msg = 'Missing parameter: {column}'.format(column=key)
		raise errors.InvalidData(msg)		
	
	user_editor_id = int(request.json[USER.EDITOR])
	user_editor = User.query.get_or_404(user_editor_id)

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

	history = history_module.edit_user(user,user_editor)
	
	response = {}
	response['user'] = user.to_dict(show_all=True)
	response['message'] = history.to_dict(show_all=True,hide=['by_user','by_user_id'])

	return (jsonify(response),200)