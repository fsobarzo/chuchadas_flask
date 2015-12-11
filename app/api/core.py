from flask import Blueprint, request, url_for, Response, jsonify, request
from app import app, db
from app import auto
from app.models.user.model import User
from datetime import datetime

mod_core = Blueprint('welcome',__name__)

#GET
@mod_core.route("/", methods = ['GET'])
def welcome():
	return (jsonify({'welcome': 'Connect to api successfully'}), 200)

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

#CREATE PLAYER
@mod_core.route("/users", methods=['POST'])
def add_chucha():
	
	user = User()
	user.username = request.json["name"]
	user.amount = 0
	user.created_at = datetime.now()
	user.updated_at = datetime.now()

	db.session.add(user)
	db.session.commit()

	response = {}
	response['user'] = user.to_dict(show_all=True)

	return (jsonify(response),201)

@mod_core.route("/users", methods=['GET'])
def show_players():
	users = User.query.all()
	users_dict = []
	if users:
		for user in users:
			users_dict.append(user.to_dict(show_all=True))

		return (jsonify({'users': users_dict}),200)

@mod_core.route("/users/<path:player>", methods=['PUT'])
def update_player(player):
	user = User.query.filter_by(username=player).first()
	print user
	user.amount = user.amount + 1

	db.session.commit()
	response = {}
	response['user'] = user.to_dict(show_all=True)
	return (jsonify(response),200)
