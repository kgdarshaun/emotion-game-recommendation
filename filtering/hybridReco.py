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
from contentBasedFiltering import recommendation as content
from collaborativeFiltering import recommendation as colloborative

games=pd.read_json('dataset/games.jl',lines=True,encoding='utf-8')

# Function to calculate hybrid recommendations
def hybrid_weight(colla_list,content_list):
    if(len(colla_list)>0) & (len(content_list)>0):
        df1 = pd.DataFrame(colla_list)
        df1.columns =['product_id','similarity']
        df2 = pd.DataFrame(content_list)
        df2.columns =['product_id','similarity']            
        joined_results= df1.merge(df2, on='product_id',how='inner')
        joined_results['weighted_avg']=(joined_results['similarity_x']*0.2)+(joined_results['similarity_y']*0.8)
        joined_results=joined_results[['product_id','weighted_avg']]
    elif len(colla_list)>0:
        joined_results = pd.DataFrame(colla_list)
        joined_results.columns =['product_id','similarity']
    elif len(content_list)>0:
        joined_results = pd.DataFrame(content_list)
        joined_results.columns =['product_id','similarity']
    else:
        joined_results = pd.DataFrame([])
        joined_results.columns =['product_id','similarity']

    return joined_results

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

def recommendation(user_id):
    # Input user recommendation
    user_id = int(user_id)
    content_list = content(user_id)
    colla_list = colloborative(user_id)

    if len(content_list) == 0 and len(colla_list) == 0:
        return pd.DataFrame()

    pred = hybrid_weight(colla_list, content_list)
    final_results = pd.DataFrame(pred)
    final_results.columns = ['product_id','weighted_avg']
    final_results = final_results.sort_values(by='weighted_avg',ascending=False)[['product_id','weighted_avg']]
    final_results = final_results.merge(games,left_on='product_id',right_on='id',how='inner')[['product_id','weighted_avg','title','tags']]
    final_results['topics']=final_results.apply(lambda x:map_tags_to_topics(x['tags']),axis=1)
    return final_results

if __name__ == "__main__":
    random_user = sys.argv[1]
    result = recommendation(random_user)
    print(result)