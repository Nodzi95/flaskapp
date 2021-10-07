import unittest
import io


# import myproject
from myproject import create_app

app = create_app()
# app = create_app()
unittest.TestLoader.sortTestMethodsUsing = None


class Monolithic(unittest.TestCase):

    APP_LOGIN = {"username": "a", "password": "a"}

    # tests rendering index page
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        # index loaded
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "text/html; charset=utf-8")

    # tests adding new user and user without user name
    def test_1_register(self):
        tester = app.test_client(self)

        # new user | user already inside db
        response = tester.post(
            "/register",
            data=dict(username="c", password="a", password2="a", follow_redirects=True),
        )
        self.assertIn(response.status_code, [200, 302])

        # username not set -> 201 code
        response = tester.post(
            "/register",
            data=dict(username="", password="a", password2="a", follow_redirects=True),
        )
        self.assertEqual(response.status_code, 201)

    # tests login and wrong login
    def test_2_login(self):
        tester = app.test_client(self)
        # login
        response = tester.post("/login", data=dict(username="c", password="a"))
        self.assertEqual(response.status_code, 302)

        # wrong password
        response = tester.post("/login", data=dict(username="a", password="b"))
        self.assertEqual(response.status_code, 201)

    # tests adding new task and adding task without name
    def test_3_add_new_task(self):
        tester = app.test_client(self)

        response = tester.post("/login", data=dict(username="c", password="a"))
        self.assertEqual(response.status_code, 302)

        # new task
        response = tester.post(
            "/task",
            data=dict(
                task_name="task 421",
                description="long description",
                finished=0,
                id=-1,
                deadline="2021-10-20",
            ),
        )
        self.assertEqual(response.status_code, 302)

        # task without name, expecting to get 303 status code -> task name wasn't set -> dont add this to the db
        response = tester.post(
            "task",
            data=dict(
                task_name="",
                description="long description",
                finished=0,
                id=-1,
                deadline="2021-10-20",
            ),
        )
        self.assertEqual(response.status_code, 303)

    # tests adding new task with attachment
    def test_4_add_task_with_attachment(self):
        tester = app.test_client(self)

        data = dict(
            task_name="task with attachment",
            description="long description",
            id=-1,
            deadline="2021-10-20",
        )
        data["attachment"] = (io.BytesIO(b"abcdef"), "test.jpg")

        # login
        response = tester.post("/login", data=dict(username="c", password="a"))
        self.assertEqual(response.status_code, 302)

        # add new task with attachment -> new task with attachment created
        response = tester.post("/task", data=data, content_type="multipart/form-data")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
