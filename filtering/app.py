from flask import Flask, request
from flask_cors import CORS
from flask_api import status
import os

from recommendations import get_recommendations

app = Flask(__name__)
CORS(app)

def validate_request(identifier):
	return identifier.isnumeric()

@app.after_request
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/recommend', methods=['POST'])
def get_user_recommendation():
	request_json = request.get_json(force=True)
	is_user = request_json['is_user']
	identifier = request_json['id']
	if validate_request(identifier):
		return get_recommendations(request_json, identifier, is_user)
	else:
		id_type = is_user if 'user' else 'steam'
		return f'"{id_type} id" must be an integer', status.HTTP_400_BAD_REQUEST


if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))