import praw
import Database.database as db

reddit = praw.Reddit('textmining')

subreddit = reddit.subreddit('politics+news+PoliticalDiscussion')

index = 0
database_handler = db.DatabaseHandler()
for submission in subreddit.hot(limit=100):
    index+=1
    print(f"Inserting submission #{index} - {submission.title}")
    if not database_handler.insert_post(submission):
        continue

    comments = submission.comments

    # Remove MoreComments instances
    comments.replace_more(limit=0)
    for comment in comments.list():
        database_handler.insert_comment(comment)


print(database_handler.get_count())

