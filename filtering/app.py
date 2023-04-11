from flask import Flask, request
from flask_cors import CORS
from flask_api import status
import os

from recommendations import get_recommendations

app = Flask(__name__)
CORS(app)

def validate_request(identifier):
	return identifier.isnumeric()

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/recommend/user/<user_id>', methods=['POST'])
def get_user_recommendation(user_id):
	if validate_request(user_id):
		request_json = request.get_json(force=True)

		return get_recommendations(request_json, user_id)
	else:
		return '"user id" must be an integer', status.HTTP_400_BAD_REQUEST


@app.route('/recommend/game/<steam_id>', methods=['POST'])
def get_game_recommendation(steam_id):
	if validate_request(steam_id):
		request_json = request.get_json(force=True)

		return get_recommendations(request_json, steam_id, False)
	else:
		return '"steam id" must be an integer', status.HTTP_400_BAD_REQUEST


if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))