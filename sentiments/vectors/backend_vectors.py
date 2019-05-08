from sentiments.vectors import helpers

import logging
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import numpy as np
from app import main

class VectorBackend:

    def __init__(self):
        if helpers.is_first_run():
            logging.info("First run detected. Running setup for vector based sentiment analysis.")
            helpers.setup()
            logging.info("First run setup complete.")

        self.negative, self.positive, self.neutral = helpers.load_vectors()

    def analyze(self, list):
        vector_array = np.empty((len(list), main.nlp.vocab.vectors_length))

        for i, text in enumerate(list):
            doc = main.nlp(text)
            vector_array[i] = doc.vector

        negative, positive, neutral = helpers.load_vectors()

        negative_result = cosine_similarity(vector_array, negative)
        positive_result = cosine_similarity(vector_array, positive)
        neutral_result = cosine_similarity(vector_array, neutral)

        result = {}
        i = 0
        for sentence in list:
            neg = negative_result[i].max()
            pos = positive_result[i].max()
            neu = neutral_result[i].max()
            computeResult = VectorBackendResult(sentence, neg, pos, neu)
            result[sentence] = computeResult
            logging.info(f"{sentence} was {computeResult.result()}")
            i = i+1

        return result

class VectorBackendResult:

    def __init__(self, text, neg, pos, neu):
        self.text = text
        self.neg = neg
        self.pos = pos
        self.neu = neu

    def result(self):
        sorted = np.array([self.neg, self.pos, self.neu]).argsort()[2]
        if sorted == 0:
            return "Negative"
        elif sorted == 1:
            return "Positive"
        elif sorted == 2:
            return "Neutral"

    def __str__(self):
        return f"{self.text} is {self.result()} || neg:{self.neg}, pos:{self.pos}, neu:{self.neu}"