from flask import Blueprint, session, request, redirect, render_template, url_for, flash
from myproject.database.db import get_user, save_user
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__)


# simple log in
@auth.route("/login", methods=("GET", "POST"))
def login():
    session.clear()
    error = None
    code = 200
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = get_user(username)

        if user is None:
            error = f"User {username} not found"
            code = 201
        elif not check_password_hash(user[2], password):
            error = "Wrong password"
            code = 201
        if error is None:

            session["user_id"] = user[0]
            session["name"] = user[1]
            return redirect(url_for("main.index"))

        flash(error)
    return render_template("login.html", error=error), code


# creates new user
@auth.route("/register", methods=("GET", "POST"))
def register():
    session.clear()
    username = ""
    password = ""
    error = ""
    code = 200
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password_repeat = request.form.get("password2")

        error = None

        if not username or not password or not password_repeat:
            code = 201
            error = "User name and password required"
        elif password != password_repeat:
            code = 201
            error = "Repeat your password correctly"

        if not error:
            error = save_user(username, password)
            if not error:
                return redirect(url_for("auth.login"))
            else:
                code = 200
    return (
        render_template(
            "register.html", username=username, password=password, error=error
        ),
        code,
    )


# clears session
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))
