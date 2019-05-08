from sentiments import analyzer
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from services.database import database_handler

queue = []

def analyze_post(post_id):
    queue.append(post_id)
    analyze_comments(post_id)

async def analyze_comments(post_id):
    print(post_id)
    comments = database_handler.get_comments(post_id)
    print(comments)
    sleep(10)

def is_being_analyzed(post_id):
    return post_id in queue