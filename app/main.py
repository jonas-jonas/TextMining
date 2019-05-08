from flask import Flask
app = Flask(__name__)

from app import routes
from app import filters
import spacy
import sentiments


nlp = spacy.load('en_core_web_lg')
sentiment = sentiments.load()

app.jinja_env.filters['polarity_class'] = filters.polarity_class
app.jinja_env.filters['subjectivity_class'] = filters.subjectivity_class
app.jinja_env.filters['is_being_analyzed'] = sentiments.analyzer.is_being_analyzed