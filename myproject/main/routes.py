from logging import error
from flask import Blueprint, session, render_template, request
from myproject.database.db import get_tasks
from myproject.tasks.utils import compareDates

main = Blueprint("main", __name__)


# index
@main.route("/", methods=["GET", "POST"])
def index():
    user = session.get("name")
    t = []
    tasks = []
    tasks.append([-1, "New task", "", ""])
    # if someone is logged, load unfinished tasks

    if session.get("user_id") != None:
        name = ""
        if request.method == "POST":
            name = request.form.get("search")

        t = get_tasks(session.get("user_id"), name=name)

        for tsk in t:
            mark = compareDates(tsk["deadline"])
            tasks.append(
                [
                    tsk["id"],
                    tsk["title"],
                    tsk["long_description"],
                    tsk["path_to_attachment"],
                    tsk["deadline"],
                    mark,
                ]
            )

    return render_template("index.html", user=user, tasks=tasks)
