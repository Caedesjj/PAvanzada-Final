from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from app.config import Config
db = SQLAlchemy()
migrate = Migrate()
from app.models import User, Project, Task, Notification, LogEntry


# import main desde app.rutas
def create_app():
    """Factory de aplicación Flask."""
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/taskflow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key-2026'
    
    db.init_app(app)
    
    # Registrar rutas
    from app.routes import init_routes
    init_routes(app)
    
    with app.app_context():
        db.create_all()
    
    return app
