from flask import Flask, request
from flask_cors import CORS
import os
import base64
from deepface import DeepFace

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/emotion', methods=['POST'])
def get_polarity():
	requestJson = request.get_json(force=True)
	image_string = requestJson['image']
	image_bytes = bytes(image_string.split(',')[1], 'UTF-8')
	with open("imageToSave.png", "wb") as fh:
		fh.write(base64.decodebytes(image_bytes))
	
	face_analysis = DeepFace.analyze(img_path = "imageToSave.png")

	return {'emotion': face_analysis[0]['dominant_emotion']}

if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
