from sentiments.text_blob import TextBlobBackend
from sentiments.vectors import VectorBackend

from services.database import database_handler
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import asyncio

backends = {
    'text_blob': TextBlobBackend(),
    'vectors': VectorBackend()
}

class SentimentAnalyzer:

    def __init__(self, backend='vectors'):
        self.backend = backend

    def analyze_comments(self, datasource):
        for sentence in datasource.values:

            text_blob_results = backends['text_blob'].analyze(sentence[0])
            
            # vectors_results = backends['vectors'].analyze(sentence[0])
            # analyzed['vectors'] = vectors_results

            save_result(sentence[1], sentence[2], text_blob_results)



def save_result(comment_id, post_id, sentiments):
    database_handler.insert_text_blob_comment_result(comment_id, post_id, sentiments.polarity, sentiments.subjectivity)



queue = []

def analyze_post(post_id):
    print(f"asd: {post_id}")
    queue.append(post_id)
    asyncio.create_task(analyze_comments(post_id))

async def analyze_comments(post_id):
    print(post_id)
    comments = database_handler.get_comments(post_id)
    print(comments)
    sleep(10)
    print("dddd")

def is_being_analyzed(post_id):
    print(post_id)
    return post_id in queue