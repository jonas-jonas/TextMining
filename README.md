# TextMining - Analysieren von Reddit Beiträgen

Das Projekt wird aus drei, in Python geschriebenen, Teilen bestehen.

## Scraper *(10%)*

Ein Programm, das periodisch die top-posts aus verschiedenen Subreddits "crawled" und diese in der Datenbank speichert.

**Benutzte APIs:**

- Praw - [https://praw.readthedocs.io/en/latest/](https://praw.readthedocs.io/en/latest/)
- psycopg2 - [http://initd.org/psycopg/](http://initd.org/psycopg/)

## Analyzer *(70%)*

Ein Programm, dass die Beiträge und Kommentare nach den folgenden Schemata analysiert:

|Beiträge|Kommentare|
|---|---|
|Themeneinordnung|Erkennung ob der Kommentar zu einer Konversation gehört|
|Kontroversität|Kontroversität|

NOTE: Beiträge können sowohl aus Texten als auch aus Links bestehen. Eventuell wird es Teil sein, den Text des Artikels auch zu Scrapen.

**APIs:**

Gensim→Topic Modelling

spaCy→Extraktion

scikit-Learn→Ähnlichkeiten, Dokumentenrepräsentation

## Presenter *(20%)*

Eine Web-Applikation, die die Ergebnisse des *Analyzers* mithilfe von Diagrammen Präsentiert.

**Artikel**:

- [http://benalexkeen.com/creating-graphs-using-flask-and-d3/](http://benalexkeen.com/creating-graphs-using-flask-and-d3/)

## Installation

_The installation istructions are currently only for Ubuntu (tested on 18.10 and 19.04)._

```
# Install required packages
sudo apt install python3-pip python-virtualenv

# Setup the virtual env
virtualenv -p /usr/bin/python3 env

# Activate the venv
source env/bin/activate

# Install the packages
pip install -r requirements.txt
```
