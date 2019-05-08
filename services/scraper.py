import praw
import services.database as db

class RedditScraper:

    def __init__(self, subreddits, access):
        self.reddit = praw.Reddit(access)
        self.subreddit = self.reddit.subreddit(subreddits)
        self.database_handler = db.DatabaseHandler()

    def save_to_database(self, count=10):
        index = 0
        for submission in self.subreddit.hot(limit=count):
            index+=1
            print(f"Inserting submission #{index} - {submission.title}")
            if not self.database_handler.insert_post(submission):
                continue

            comments = submission.comments

            # Remove MoreComments instances
            comments.replace_more(limit=0)
            for comment in comments.list():
                self.database_handler.insert_comment(comment)

    def print_count(self):
        print(self.database_handler.get_count())
