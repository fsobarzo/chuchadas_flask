from flask import jsonify, request
from app import app

class InvalidData(Exception):
	status_code = 400
	message = 'No data/json sent'
	def __init__(self, message=None, payload=None):
		Exception.__init__(self)
		if message is not None:
			self.message = message
		self.payload = payload
	
	# def to_dict(self):
	# 	rv = dict(self.payload or ())
	# 	rv['message'] = self.message
	# 	return rv

@app.errorhandler(404)
def not_found(e):
	msg = {
	  "status": 404,
		"message": "Not Found",
		"url": request.url
	}
	response = jsonify(msg)
	response.status_code = 404
	return response

@app.errorhandler(InvalidData)
def no_data(e):
	msg = {
	  "status": e.status_code,
	  "message": e.message,
		"url": request.url
	}
	response = jsonify(msg)
	response.status_code = 400
	return response