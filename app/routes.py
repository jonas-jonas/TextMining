from .main import app
from flask import render_template, redirect
from services.database import database_handler as db
from services.analyzer import analyze_post

@app.route("/")
def index():
    posts = db.get_posts(limit=20)
    return render_template("index.html", posts=posts)


@app.route("/post/<id>")
def post(id):
    post = db.get_post(id)
    comments = db.get_comments(id, limit=10)

    # test_comment = comments[2]

    # md_link = r"/__|\#|(?:\[([^\]]*)\]\([^)]*\))"
    # md_quote = r"\>(.*?)\\n"

    # print(test_comment)
    # print(find_parsed(md_quote, test_comment))

    return render_template("post.html", post = post, comments = comments)

@app.route("/post/<id>/analyze")
def get_analyze_post(id):
    analyze_post(id)
    return redirect(f'/post/{id}')

# def find_parsed(regex, string):
#     xx = re.search(regex, str(string))
#     if xx is None:
#         return "<nothing found>"
#     else:
#         return xx.group(1)
