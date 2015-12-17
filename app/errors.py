from flask import jsonify, request
import app

@app.errorhandler(404)
def not_found(e):
	message = {
	  "status": 404,
		"message": "Not Found",
		"url": request.url
	}
	response = jsonify(message)
	response.status_core = 404
	return response