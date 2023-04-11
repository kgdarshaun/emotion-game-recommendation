import pandas as pd
import sys
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import pandas as pd
import gensim
import sys
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
from gensim.corpora import Dictionary
np.random.seed(2018)
import pickle
nltk.download('omw-1.4')
nltk.download('wordnet')
import ast

game_df_original = pd.read_json('../dataset/games.jl', lines=True, encoding='utf-8')

# Function to lemmatize text
def lemmatize_and_stem(word):
    stemmer = SnowballStemmer(language='english')
    return stemmer.stem(WordNetLemmatizer().lemmatize(word, pos='v'))

# unction to preprocess text
def preprocess_text(text):
    try:
        text=ast.literal_eval(str(text))
        text=' '.join(text)
        result_tag = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                result_tag.append(lemmatize_and_stem(token))
        return result_tag 
    except ValueError:
        return 'NA'

# Mapping topics to games suggested to a user
def map_tags_to_topics(unseen_game_tag):
    unseen_game_tag = str(unseen_game_tag)
    bow_vector = dictionary.doc2bow(preprocess_text(unseen_game_tag))
    topics_list=list()
    for index, score in sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1]):
        topics_list.append(index)
    return topics_list
    
# Loading the dictionary creates through LDA
dictionary = Dictionary.load('lda_dict.dict')

with open("lda_model.pkl", "rb") as f:
    lda_model = pickle.load(f)

#Function to find recommendations for a new user given a game id from steam
def recommendation(steam_id):
    steam_id = int(steam_id)
    # Create a dataframe of tags for content based filtering
    game_df = game_df_original[['tags','id']].dropna(subset=['tags', 'id'])
    game_df = game_df.assign(genres=game_df['tags'].str.split(', ')).explode('tags')
    game_df = game_df[['tags','id']]
    one_hot_df = pd.get_dummies(game_df['tags'], prefix='tags')
    result_df = pd.concat([game_df['id'], one_hot_df], axis=1)
    df_tags = result_df.groupby('id').sum()
    df_tags.index = df_tags.index.astype(int)

    #creaiting vector of the given game
    random_vec=df_tags[df_tags.index==steam_id]

    if len(random_vec) == 0:
        return pd.DataFrame()

    # Finding similarity between user profile and games (via tags)
    cos_sim = cosine_similarity(random_vec, df_tags)
    cos_sim_df = pd.DataFrame(
        {'cosine_similarity': cos_sim[0], 'ind': df_tags.index})

    # Making sure already playes games are not recommended
    reco_games = cos_sim_df[~(cos_sim_df.ind.isin([steam_id]))]

    reco_games.set_index('ind', inplace=True)
    final_game_suggestions = game_df_original[game_df_original.id.isin(
        reco_games.index)][['id']]
    final_game_suggestions = final_game_suggestions.merge(
        reco_games, left_on='id', right_on='ind')[['id', 'cosine_similarity']]
    final_game_suggestions = final_game_suggestions
    final_results = final_game_suggestions.merge(game_df_original,on='id',how='inner')[['id','cosine_similarity','title','tags']].sort_values(by='cosine_similarity',ascending=False)
    
    #Changing column names for uniformity
    final_results = final_results.rename(columns={'id': 'product_id', 'cosine_similarity': 'weighted_avg'})
    final_results['topics']=final_results.apply(lambda x:map_tags_to_topics(x['tags']),axis=1)
    return final_results[['product_id','weighted_avg','title','tags','topics']]
    
if __name__ == "__main__":
    steam_id = sys.argv[1]
    result = recommendation(steam_id)
    print(result)