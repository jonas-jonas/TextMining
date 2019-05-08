import spacy
import numpy as np
from pathlib import Path
import logging
from app import main

sentiments_directory = 'data/sentiments'

subjectivity_file = sentiments_directory + '/subjectivity.ttf'

files = {
    'negative': sentiments_directory + '/negative.txt',
    'positive': sentiments_directory + '/positive.txt',
    'neutral': sentiments_directory + '/neutral.txt'
}

vector_files = {
    'negative': sentiments_directory + '/negative-vector.txt',
    'positive': sentiments_directory + '/positive-vector.txt',
    'neutral': sentiments_directory + '/neutral-vector.txt'
}

def extract_lexicon():
    """
        Extracts all words with their sentiment into seperate arrays.
    """
    logging.info("Extracting lexicons from subjectivity file")
    file = open(subjectivity_file, "r")
    if not file.is_file():
        raise FileNotFoundError("Couldn't find subjectivity file. Please download the file and put it in data/sentiments from http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/.")

    lines = file.readlines()
    negativeFile = open(files['negative'], 'w')
    positiveFile = open(files['positive'], 'w')
    neutralFile = open(files['neutral'], 'w')
    for line in lines:
        sentiment = ''
        word = ''
        for entry in line.split(" "):
            s = entry.split("=")
            if s[0] == 'priorpolarity':
                sentiment = s[1]
            elif s[0] == 'word1':
                word = s[1]

        if(sentiment == 'negative\n'):
            negativeFile.write(word + '\n')
        elif sentiment == 'positive\n':
            positiveFile.write(word + '\n')
        elif sentiment == 'neutral\n':
            neutralFile.write(word + '\n')
        elif sentiment == 'both\n':
            positiveFile.write(word + '\n')
            negativeFile.write(word + '\n')

def load_lexicons():
    negative = []
    positive = []
    neutral = []
    with open(files['negative']) as f:
        negative.extend(f.read().splitlines())

    with open(files['positive']) as f:
        positive.extend(f.read().splitlines())

    with open(files['neutral']) as f:
        neutral.extend(f.read().splitlines())
    
    return negative, positive, neutral


def get_noun_vector(list, nlp):
    vector_list = [nlp.vocab[word].vector for word in list]
    vectors = np.array(vector_list)
    return vectors

def generate_vectors():
    logging.info("Generating noun vectors for lexicons")
    negative, positive, neutral = load_lexicons()

    negative_vector = get_noun_vector(negative, main.nlp)
    positive_vector = get_noun_vector(positive, main.nlp)
    neutral_vector = get_noun_vector(neutral, main.nlp)
    return negative_vector, positive_vector, neutral_vector

def save_vectors():
    negative_vector, positive_vector, neutral_vector = generate_vectors()
    np.savetxt(vector_files['negative'], negative_vector)
    np.savetxt(vector_files['positive'], positive_vector)
    np.savetxt(vector_files['neutral'], neutral_vector)


def load_vectors():
    negative_vector = np.loadtxt(vector_files['negative'])
    positive_vector = np.loadtxt(vector_files['positive'])
    neutral_vector = np.loadtxt(vector_files['neutral'])
    return negative_vector, positive_vector, neutral_vector

def is_first_run():
    # Check if vector files exist
    result = True
    for _, value in vector_files.items():
        path = Path(value)
        result = path.is_file()
    return not result

def setup():
    extract_lexicon()
    save_vectors()
