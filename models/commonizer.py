import spacy
import string
import pandas as pd

import services.database
from collections import Counter

from bokeh.plotting import figure
from bokeh.embed import components

punctuations = string.punctuation + "’‘"

class Commononizer():

    def __init__(self, data):
        self.data = data

    def commonize(self, logging=False):
        result = cleanup_text(self.data, logging)
        result = ' '.join(result).split()

        counts = Counter(result)

        common_words = [word[0] for word in counts.most_common(20)]
        common_counts = [word[1] for word in counts.most_common(20)]

        plot = figure(sizing_mode='stretch_both', x_range=common_words, title="Frequency of words")
        plot.vbar(x=common_words, width=0.75, bottom=0, top=common_counts, color="#5d7bd0", )
        plot.toolbar.logo = None
        plot.toolbar_location = None

        return components(plot)

def cleanup_text(docs, logging=False):
    nlp = spacy.load('en_core_web_sm')
    texts = []
    counter = 1
    for doc in docs:
        if counter % 60 == 0 and logging:
            print("Processed %d out of %d documents." % (counter, len(docs)))
        counter += 1
        doc = nlp(doc, disable=['parser', 'ner'])
        tokens = [tok.lemma_.lower().strip() for tok in doc if tok.lemma_ != '-PRON-' and not tok.is_stop]
        tokens = [tok for tok in tokens if tok not in punctuations]
        tokens = ' '.join(tokens)
        texts.append(tokens)
    return pd.Series(texts)
