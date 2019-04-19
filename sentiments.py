fileName = "./data/sentiments.tff"

negative = []
positive = []

def read_lexicons():
    file = open(fileName, "r")
    lines = file.readlines()
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
            negative.append(word)
        elif sentiment == 'positive\n':
            positive.append(word)


read_lexicons()