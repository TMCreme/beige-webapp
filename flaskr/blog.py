"""
Management of the blog posts
"""
from flask import (
    Blueprint, render_template
)

from .db import get_db


bp = Blueprint('blog', __name__)


@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route("/create")
def create():
    return {"message": "Welcome"}


@bp.route("/update")
def update():
    return {"message": "Welcome"}
