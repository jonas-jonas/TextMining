# TODO: Load config from file
import os
from configparser import ConfigParser
import queries
import praw
from datetime import datetime

SCRIPT_DIR = os.path.dirname(__file__)

SCHEMA_FOLDER = os.path.join(SCRIPT_DIR, "schema")

class DatabaseHandler():

    def __init__(self):
        # Read the configuration from the database
        parser = ConfigParser()
        parser.read('Database/database.ini')
        if parser.has_section('postgres'):
            params = parser._sections['postgres']
            connection_string = queries.uri(**params)
        else:
            raise Exception(f'Section "postgres" not found in file Database/database.ini')
        # Set the queries.Session object as a field on the class for reuse
        self.session = queries.Session(connection_string)

    def insert_post(self, submission: praw.models.Submission):
        """Inserts a Submission object into the database.

        Inserts the fields id, subreddit, selftext, url, title and created_utc
        of a :func:`praw.models.Submission` object into the database.
        If the selftext of the submission is empty it is replaced with null
        in the database.
        The created_utc is transformed into a timestamp by the datetime package.

        Args:
            submission: the submision that should be inserted. It should be of type
                :func:`praw.models.Submission`. Otherwise the method returns and a message
                indicating that the passed object was of a wrong type is printed.

        Returns:
            True: if the records was succesfully inserted
            False: if there was an error while inserting
        """
        if not isinstance(submission, praw.models.Submission):
            print(f"post with id {submission.id} is not of correct type. Excpected praw.models.Submission.")
            return

        selftext = submission.selftext if submission.selftext else "null"
        insertquery = f'''
            INSERT INTO post (id, subreddit, selftext, url, title, created_utc)
            VALUES (
                '{submission.id}',
                '{submission.subreddit.display_name}',
                $${selftext}$$,
                $${submission.url}$$,
                $${submission.title}$$,
                '{datetime.fromtimestamp(submission.created_utc)}'
            );
        '''
        try:
            results = self.session.query(insertquery)
        except (queries.IntegrityError, queries.DataError) as error:
            print(f'Caught Error: {error.pgerror}')
            return False
        else:
            if not results:
                return False
            else: 
                return True

    def insert_comment(self, comment: praw.models.Comment):
        """Inserts a Comment into the database.
        """
        if not isinstance(comment, praw.models.Comment):
            print(f"comment with id {comment.id} is not of correct type. Expected praw.models.Comment. Got {type(comment)}.")
            return

        parent_id = "null" if comment.parent_id.startswith("t3_") else f"'{comment.parent().id}'"

        # Escape any $ with a \
        comment_body = comment.body.replace('$', r'\$')

        insertquery = f'''
            INSERT INTO comment (id, body, post_id, subreddit, parent_id, created_utc)
            VALUES (
                '{comment.id}', 
                $${comment_body}$$,
                '{comment.submission.id}',
                '{comment.submission.subreddit.display_name}',
                {parent_id},
                '{datetime.fromtimestamp(comment.created_utc)}'
            );
        '''
        try:
            results = self.session.query(insertquery)
        except (queries.IntegrityError, queries.DataError) as error:
            print(f'Caught Error: {error.pgerror}')
            return False
        else:
            if not results:
                return False
            else: 
                return True

    def get_count(self): 
        query = "SELECT 'Comments' AS Type, Count(*) FROM COMMENT UNION SELECT 'Posts' AS Type, COUNT(*) FROM Post;"

        results = self.session.query(query)
        for x in results:
            print(x)
