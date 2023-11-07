"""
APIs for the user auth
"""
from flask import (
    Blueprint, request, flash, jsonify
)
from werkzeug.security import generate_password_hash

from .db import get_db


bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")


@bp.route("/register", methods=("POST", ))
def register():
    """API for Registration of users"""
    username = request.form["username"]
    password = request.form["password"]
    db = get_db()
    error = None

    if not username:
        error = "Username is required"
    elif not password:
        error = "Password is required"
    if error is None:
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered"
            return jsonify({"error": error})

    return jsonify({"message": "Successfully added user"})


@bp.route("/users", methods=("GET", ))
def users():
    """All users endpoint"""
    db = get_db()
    try:
        users = db.execute(
            "SELECT id, username FROM user ORDER BY id"
        ).fetchall()
    except Exception as e:
        return jsonify({"error": f"Error occurred: {e}"})
    all_users = []
    for user in users:
        all_users.append({
            "id": user["id"],
            "username": user["username"]
        })
    # print(all_users["username"])
    return jsonify(all_users)
