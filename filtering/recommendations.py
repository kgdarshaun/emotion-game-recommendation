
import json
import requests as rq

from hybridReco import recommendation as user_recommendation
from newUserReco import recommendation as game_recommendation

emotion_to_topic = json.loads(open('emotion_to_topic.json', 'r').read())
emotion_to_genre = json.loads(open('emotion_to_genre.json', 'r').read())


emotion_detection_url = 'http://localhost:8081/emotion'


def get_emotion(request_json):
	return rq.post(emotion_detection_url, json=request_json).json()['emotion']

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