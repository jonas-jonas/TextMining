import spacy

import psycopg2 as pg
import pandas.io.sql as psql
import Database.database as db
import pandas as pd
import numpy as np

ID = 'b79598'

# get connected to the database
#connection = db.DatabaseHandler().session.connection
 
#dataframe = psql.read_sql(f"""
#    SELECT c.body as body
#    FROM post p LEFT JOIN comment c ON c.post_id = p.id WHERE p.id = '{ID}';""", connection)

#body = dataframe['body']

from sentiments import negative, positive
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

comp = ["This just nice and awesome", "Fuck this shit"]

nlp = spacy.load('en_core_web_lg')
vector_array = np.empty((len(comp), nlp.vocab.vectors_length))

for i, text in enumerate(comp):
    doc = nlp(text)
    vector_array[i] = doc.vector

def get_noun_vector(list):
    vector_list = [nlp.vocab[word].vector for word in list]
    vectors = np.array(vector_list)
    return np.mean(vectors, axis = 0).reshape(-1, 300)

x = get_noun_vector(negative)

print(cosine_similarity(vector_array, x))