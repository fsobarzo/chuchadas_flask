from flask import Blueprint, request, jsonify, request
from app import app, db
from app import auto
from app.models.user.model import User
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
def show_players():
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
	if "name" not in request.json:
		return (jsonify({"error":"Faltan datos"}),400)

	user = User()
	user.username = request.json["name"]
	db.session.add(user)
	db.session.commit()
	
	response = {}
	response['user'] = user.to_dict(show_all=True)
	return (jsonify(response),201)

#METHODS: PUT
#DESCRIPTION: EDITAR USUARIO
@mod_core.route("/users/<path:player>/chuchada", methods=['PUT'])
def update_player(player):
	user = User.query.filter_by(username=player).first()
	if not user:
		return (jsonify({"error":"Usuario no existe"}),400)

	quantity = 1
	if request.json and "quantity" in request.json:
		quantity = int(request.json["quantity"])
		if quantity < 0:
			return (jsonify({"error":"Cantidad menor a 1"}))

	user.quantity+= quantity
	user.amount+= quantity*USER.VALUE
	user.updated_at = datetime.now()
	db.session.commit()

	response = {}
	response['user'] = user.to_dict(show_all=True)
	return (jsonify(response),200)

#METHODS: PUT
#DESCRIPTION: EDITAR NOMBRE USUARIO
@mod_core.route("/users/<int:user_id>",methods=["PUT"])
def update_user(user_id):
	if not request.json:
		return (jsonify({"error":"Data no enviada"}),400)

	user = User.query.get(user_id)
	if not user:
		return (jsonify({"error":"Usuario no existe"}),400)
	
	params = user.to_dict(show_all=True,hide=["created_at","updated_at"])
	for key in USER.COLUMNS:
		if key in request.json:
			params[key] = request.json[key]

	user.username   = params[USER.USERNAME]
	user.quantity   = params[USER.QUANTITY]
	user.amout      = params[USER.QUANTITY]*USER.VALUE
	user.updated_at = datetime.now()
	db.session.commit()

	return (jsonify({"user":user.to_dict(show_all=True)}),200)