from shutil import ExecError
import sqlite3
import os

UPLOADS = os.path.join(os.path.dirname(__file__), "uploads")

DB = os.path.join(os.path.dirname(__file__), "deso.sqlite")

try:

    if os.path.exists(UPLOADS):
        import shutil

        shutil.rmtree(UPLOADS)
        print("SUCCESSFULLY DELETED OLD FILES")
except Exception as e:
    print(e)


conn = sqlite3.connect(DB)

cursor = conn.cursor()

createUser = """CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL

);"""

createTask = """CREATE TABLE task(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    long_description TEXT,
    path_to_attachment TEXT,
    finished BIT NOT NULL DEFAULT 0,
    deadline TEXT,
    completed TEXT,
    FOREIGN KEY (author_id) REFERENCES user(id)
);"""

dropUser = "DROP TABLE IF EXISTS user;"
dropTasks = "DROP TABLE IF EXISTS task;"

cursor.execute(dropUser)
cursor.execute(dropTasks)

cursor.execute(createUser)
cursor.execute(createTask)
