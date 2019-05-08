CREATE TABLE IF NOT EXISTS post (
    id VARCHAR(255) NOT NULL,
    subreddit VARCHAR(20) NOT NULL,
    selftext TEXT,
    url TEXT,
    title TEXT NOT NULL,
    created_utc TIMESTAMP NOT NULL,
    inserted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_post_id_subreddit PRIMARY KEY (id, subreddit)
);

CREATE TABLE IF NOT EXISTS comment (
    id VARCHAR(255) NOT NULL,
    body TEXT NOT NULL,
    post_id VARCHAR(255) NOT NULL,
    subreddit VARCHAR(20) NOT NULL,
    parent_id VARCHAR(255),
    created_utc TIMESTAMP NOT NULL,
    inserted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_comment_id_post_id PRIMARY KEY (id, post_id),
    CONSTRAINT fk_parent_id_comment FOREIGN KEY (parent_id, post_id) REFERENCES comment(id, post_id),
    CONSTRAINT fk_post_id_post FOREIGN KEY (post_id, subreddit) REFERENCES post(id, subreddit)
);

CREATE SCHEMA IF NOT EXISTS sentiment;

CREATE TABLE IF NOT EXISTS sentiment.comment_text_blob (
    comment_id VARCHAR(255) NOT NULL,
    post_id VARCHAR(255) NOT NULL,
    polarity DECIMAL(501, 500),
    subjectivity DECIMAL(201, 200),
    CONSTRAINT pk_comment_comment_id_post_id PRIMARY KEY (comment_id, post_id)
)