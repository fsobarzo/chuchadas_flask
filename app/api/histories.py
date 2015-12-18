from flask import Blueprint, request, jsonify, request
from app.models.user.model import User
from app.models.history.model import History
from datetime import datetime

mod_history = Blueprint('history',__name__)

#ADD PAGINATION

#METHODS: GET
#DESCRIPTION: HISTORIA
#TODO: CARGAR TODAS LAS HISTORIAS
@mod_history.route('/histories/',methods=["GET"])
def get_all_histories():
	histories = History.query.order_by(History.id.desc()).limit(15).all()
	return (jsonify({'histories': [history.to_dict(show_all=True) for history in histories] }),200)

#METHODS: GET
#DESCRIPTION: HISTORIA
#TODO: CARGAR HISTORIAS USUARIO
@mod_history.route('/histories/<int:user_id>',methods=["GET"])
def get_user_histories(user_id):
	user = User.query.get_or_404(user_id)
	histories = History.query.filter(History.by_user_id == user.id)
	histories = histories.order_by(History.id.desc()).limit(15).all()
	return (jsonify({'histories': [history.to_dict(show_all=True) for history in histories] }),200)