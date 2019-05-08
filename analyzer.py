import spacy

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
import numpy as np
from services.database import database_handler

ID = 'b79598'

connection = database_handler.session.connection
 
dataframe = psql.read_sql(f"""
   SELECT c.body as body
   FROM post p LEFT JOIN comment c ON c.post_id = p.id WHERE p.id = '{ID}';""", connection)

comp = dataframe['body']


from services.sentiments import load_vectors, load_lexicons
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#comp = ["You be fuck stupid", "Nice work mate", "Cool stuff"]

nlp = spacy.load('en_core_web_lg')
# Array of vectors from the sentence
vector_array = np.empty((len(comp), nlp.vocab.vectors_length))

for i, text in enumerate(comp):
    doc = nlp(text)
    vector_array[i] = doc.vector

negative, positive, neutral = load_vectors()
negative_words, positive_words, neutral_words = load_lexicons()

negative_result = cosine_similarity(vector_array, negative)
positive_result = cosine_similarity(vector_array, positive)
neutral_result = cosine_similarity(vector_array, neutral)

def get_result(array):
    result = np.sort(array)[-5::]
    return array.ptp()

def get_sentiment(neg, pos, neu):
    sorted = np.array([neg, pos, neu]).argsort()[2]
    if sorted == 0:
        return "Negative"
    elif sorted == 1:
        return "Positive"
    elif sorted == 2:
        return "Neutral"


i = 0
for sentence in comp:
    n = get_result(negative_result[i])
    p = get_result(positive_result[i])
    neutral = get_result(neutral_result[i])
    print(f"{sentence} is {get_sentiment(n, p, neutral)}: \nPositive={p} \nNegative={n} \nNeutral ={neutral}")
    i = i+1