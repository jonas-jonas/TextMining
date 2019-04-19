import spacy
nlp = spacy.load("en_core_web_lg")
doc = nlp(u"This is a sentence.")
print([(w.text, w.pos_) for w in doc])