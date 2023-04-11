
import json
import base64
from deepface import DeepFace


from hybridReco import recommendation as user_recommendation
from newUserReco import recommendation as game_recommendation

emotion_to_topic = json.loads(open('emotion_to_topic.json', 'r').read())
emotion_to_genre = json.loads(open('emotion_to_genre.json', 'r').read())


## To initiate download of pretrained datasets
DeepFace.analyze(img_path = "Image.jpg")

def get_emotion(request_json):
	image_string = request_json['image']
	image_bytes = bytes(image_string.split(',')[1], 'UTF-8')
	with open("imageToSave.png", "wb") as fh:
		fh.write(base64.decodebytes(image_bytes))
	
	face_analysis = DeepFace.analyze(img_path = "imageToSave.png")

	return face_analysis[0]['dominant_emotion']

def filter_recommendations(recommendations, emotion):
	mapped_topic = emotion_to_topic[emotion]

	filtered_recommendataions = recommendations[recommendations['topics'].apply(lambda x: mapped_topic in x)]

	filtered_recommendataions['product_id'].astype('int')

	return {
		'games': json.loads(filtered_recommendataions.head(3)[['product_id', 'title']].to_json(orient='records')),
		'emotion': emotion
	}

def get_recommendations(request_json, indentifier, is_user=True):
	emotion = get_emotion(request_json)

	recommender = user_recommendation if is_user else game_recommendation

	recommendations = recommender(indentifier)

	if recommendations.empty:
		return {
			'games': json.loads('[]'),
			'emotion': emotion
		}

	filtered_recommendations = filter_recommendations(recommendations, emotion)

	return filtered_recommendations