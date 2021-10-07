import os
from flask import request, current_app, session
from datetime import datetime, date

# uploads file to the server
def upload_file(last_id, filename):
    uploads_dir = os.path.join(current_app.root_path, "uploads")
    user_dir = os.path.join(uploads_dir, str(session.get("user_id")))
    task_dir = os.path.join(user_dir, str(last_id))

    # remove old content
    try:
        if os.path.exists(task_dir):
            import shutil

            shutil.rmtree(task_dir)
    except Exception as e:
        print("Old directory can't be removed")

    # create new folder
    try:
        os.makedirs(task_dir)

        profile = request.files["attachment"]
        profile.save(os.path.join(task_dir, filename))
    except OSError as error:
        print("Directory can't be created, file not saved")


# compare deadline and today
def compareDates(deadline):
    mark = "ok"
    if deadline != "":
        date1 = datetime.strptime(deadline, "%Y-%m-%d")
        date2 = datetime.strptime(str(date.today()), "%Y-%m-%d")
        diff = (date1 - date2).days

        if diff > 2:
            mark = "ok"
        elif diff <= 2 and diff >= 0:
            mark = "warning"
        else:
            mark = "late"
    return mark
