from flask import (
    Blueprint,
    session,
    request,
    redirect,
    url_for,
    send_from_directory,
    abort,
    current_app,
    render_template,
)
from myproject.database.db import (
    save_task,
    get_id_of_last_inserted,
    update_task,
    delete_task,
    get_tasks,
)
from myproject.tasks.utils import upload_file
from werkzeug.utils import redirect, secure_filename
import os
from datetime import date
from myproject.tasks.utils import compareDates


tasks = Blueprint("tasks", __name__)

# creating and editing tasks
@tasks.route("/task", methods=["POST"])
def task():

    if request.method == "POST":
        task_name = request.form.get("task_name")
        description = request.form.get("description")

        deadline = request.form.get("deadline")

        finished = 0
        completed = ""
        if request.form.get("finished"):
            finished = 1
            completed = str(date.today())

        id = request.form.get("id")

        error = None
        f = False
        filename = ""

        code = 302
        # checks if task name inserted
        if not task_name:
            error = "Task name required"
            code = 303
            return redirect(url_for("main.index"), code=code)

        # checks if user wants to upload file
        if "attachment" in request.files:
            file = request.files["attachment"]
            if file.filename != "":
                f = True
                filename = secure_filename(file.filename)
                code = 302

        # new task
        if int(id) == -1:
            error = save_task(
                session.get("user_id"),
                task_name,
                description,
                filename,
                finished=finished,
                deadline=deadline,
                completed=completed,
            )
            if error == -1:
                abort(404)
            last_id = get_id_of_last_inserted()

            if f:
                upload_file(last_id, filename)

            return redirect(url_for("main.index"), code=code)

        # edit task
        else:
            error = update_task(
                id,
                task_name,
                description,
                filename,
                finished=finished,
                deadline=deadline,
                completed=completed,
            )
            if error == -1:
                abort(404)
            if f:
                upload_file(id, filename)

        if error:
            code = 303

        return redirect(url_for("main.index"), code=code)


# deletes task from db also removes files and directories from server
@tasks.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        id = request.form.get("id")
        if delete_task(int(id)) == -1:
            abort(404)
        uploads_dir = os.path.join(current_app.root_path, "uploads")
        user_dir = os.path.join(uploads_dir, str(session.get("user_id")))
        task_dir = os.path.join(user_dir, id)

        try:
            import shutil

            shutil.rmtree(task_dir)
        except Exception as e:
            print("Directory with file can't be removed")

    return redirect(url_for("main.index"))


# download attachment
@tasks.route("/uploads/<path:filename>", methods=["GET", "POST"])
def download_file(filename):
    id = session.get("user_id")
    uploads_dir = os.path.join(current_app.root_path, "uploads")
    UPLOADS = os.path.join(uploads_dir, str(id))

    try:
        return send_from_directory(UPLOADS, filename, as_attachment=True)
    except Exception as e:
        print(e)
        abort(404)


@tasks.route("/finished", methods=["GET", "POST"])
def finished():
    user = session.get("name")
    t = []
    tasks = []
    # if someone is logged, load finished tasks
    if session.get("user_id") != None:
        name = ""
        if request.method == "POST":
            name = request.form.get("search")
        t = get_tasks(session.get("user_id"), name=name, finished=1)
        if t == -1:
            abort(404)
        for tsk in t:
            mark = compareDates(tsk["deadline"])
            if mark != "late":
                mark = "ok"
            tasks.append(
                [
                    tsk["id"],
                    tsk["title"],
                    tsk["long_description"],
                    tsk["path_to_attachment"],
                    tsk["deadline"],
                    tsk["completed"],
                    mark,
                ]
            )
    return render_template("finished.html", user=user, tasks=tasks)
