import os
import sqlite3
from werkzeug.security import generate_password_hash
from flask import current_app
from myproject.db_init import db_init


def get_db():
    conn = None
    new = False
    try:
        if not os.path.isfile(current_app.config["DATABASE"]):
            new = True
        conn = sqlite3.connect(current_app.config["DATABASE"])
        if new:
            db_init()
    except sqlite3.Error as e:
        print(e)
    return conn


def get_all():
    db = get_db()
    if db == None:
        return -1
    return db.execute(f"SELECT * FROM user").fetchall()


def get_user(user=None):
    db = get_db()
    if db == None:
        return -1
    return db.execute(f"SELECT * FROM user WHERE username='{user}'").fetchone()


def save_user(user=None, password=None):
    error = None
    db = get_db()
    if db == None:
        return -1
    try:
        db.execute(
            f"INSERT INTO user (username, password) VALUES ('{user}', '{generate_password_hash(password)}')"
        )
        db.commit()
    except db.IntegrityError:
        error = f"User {user} is already registered, try different user name"

    return error


def save_task(
    author_id,
    title,
    long_description,
    path_to_attachment,
    finished=0,
    deadline="",
    completed="",
):
    error = None
    db = get_db()
    if db == None:
        return -1

    try:
        db.execute(
            f"INSERT INTO task (author_id, title, long_description, path_to_attachment, finished, deadline, completed) VALUES ({author_id}, '{title}', '{long_description}', '{path_to_attachment}', {finished}, '{deadline}', '{completed}')"
        )
        db.commit()
    except db.IntegrityError:
        error = f"Something went wrong with saving {title}"

    return error


def get_file(id):
    db = get_db()
    if db == None:
        return -1
    return db.execute(f"SELECT path_to_attachment FROM task WHERE id={id}").fetchone()


def update_task(
    id, title, long_description, path_to_attachment, finished, deadline="", completed=""
):
    error = None
    db = get_db()
    if db == None:
        return -1
    if path_to_attachment == "":
        path_to_attachment = get_file(id)[0]
    elif path_to_attachment == -1:
        path_to_attachment = ""
    try:
        db.execute(
            f"UPDATE task SET title=coalesce('{title}', title), long_description='{long_description}', path_to_attachment='{path_to_attachment}', finished={finished}, deadline='{deadline}', completed='{completed}' WHERE id={id}"
        )
        db.commit()
    except db.IntegrityError:
        error = f"Something went wrong with saving {title}"

    return error


def get_tasks(author_id, name="", finished=0):
    db = get_db()
    if db == None:
        return -1
    db.row_factory = sqlite3.Row
    c = db.cursor()
    query = ""
    if name == "":
        query = (
            f"SELECT * FROM task WHERE author_id={author_id} and finished={finished}"
        )
    else:
        query = f"SELECT * FROM task WHERE author_id={author_id} and finished={finished} and title LIKE  '%{name}%'"
    return c.execute(query).fetchall()


def get_id_of_last_inserted():
    db = get_db()
    if db == None:
        return -1
    id = db.execute("SELECT max(id) FROM task").fetchone()
    return id[0]


def delete_task(id):
    db = get_db()
    if db == None:
        return -1

    db.execute(f"DELETE FROM task WHERE id={id}")
    db.commit()
