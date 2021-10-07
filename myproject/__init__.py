# TODO handle checkbutton for completing tasks
# TODO css zarovnat check button a delete button


from flask import Flask, session
from myproject.tasks.routes import tasks
from myproject.main.routes import main
from myproject.users.routes import auth
from myproject.errors.handlers import errors
from myproject.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(tasks)
    app.register_blueprint(errors)

    return app
