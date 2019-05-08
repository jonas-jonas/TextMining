from textblob import TextBlob

class TextBlobBackend:

    def __init__(self):
        self.name = 'TextBlob'

    def analyze(self, text):
        return TextBlob(text).sentiment