# TODO: Load config from file
import os
from configparser import ConfigParser
import queries
import praw
from datetime import datetime
from app import main

SCRIPT_DIR = os.path.dirname(__file__)

SCHEMA_FOLDER = os.path.join(SCRIPT_DIR, "services/database/schema")

class DatabaseHandler():

    def __init__(self):
        # Read the configuration from the database
        parser = ConfigParser()
        parser.read('database.ini')
        if parser.has_section('database'):
            params = parser._sections['database']
            connection_string = queries.uri(**params)
        else:
            raise Exception(f'Section "database" not found in file database.ini')
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
            return results is not None

    def get_count(self): 
        query = " SELECT 'Posts' AS Type, COUNT(*) FROM Post UNION SELECT 'Comments' AS Type, Count(*) FROM COMMENT;"

        results = self.session.query(query)
        return results.items()

    def get_posts(self, limit=0):
        query = f"""
            SELECT p.id, p.title, p.subreddit, p.url, COUNT(c.id) as comments
            FROM post p
            JOIN comment c
            ON c.post_id = p.id
            GROUP BY p.id, p.title, p.subreddit, p.url
            LIMIT {'ALL' if limit == 0 else limit};
        """

        results = self.session.query(query)
        return results.items()

    def get_post(self, id):
        query = f"""
            SELECT p.id, p.title, p.selftext, p.url, p.subreddit, (
                SELECT COUNT(1) FROM sentiment.comment_text_blob WHERE post_id = '{id}'
                ) as analyzed_comments
            FROM post p
            WHERE p.id = '{id}';
        """

        results = self.session.query(query)
        return results[0]

    def get_comments(self, id, limit=0):
        query = f"""
            SELECT c.id, c.body, CAST(tb.polarity as DECIMAL(4,2)), CAST(tb.subjectivity as DECIMAL(4,2))
            FROM comment c
            LEFT OUTER JOIN sentiment.comment_text_blob tb
            ON c.id = tb.comment_id AND c.post_id = tb.post_id
            WHERE c.post_id = '{id}'
            LIMIT {'ALL' if limit == 0 else limit};
        """

        results = self.session.query(query)
        return results.items()

    def insert_text_blob_comment_result(self, comment_id, post_id, polarity, subjectivity):
        query = f"""
            INSERT INTO sentiment.comment_text_blob
            (comment_id, post_id, polarity, subjectivity)
            VALUES
            ('{comment_id}', '{post_id}', {polarity}, {subjectivity})
        """

        self.session.query(query)
