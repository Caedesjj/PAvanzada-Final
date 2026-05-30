from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from app.config import Config
db = SQLAlchemy()
migrate = Migrate()
from app.models import User, Project, Task, Notification, LogEntry


# import main desde app.rutas
def create_app():

    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    return app
