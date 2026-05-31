import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    # Crear la carpeta instance si no existe
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Construir la ruta completa de la base de datos
    db_path = os.path.join(app.instance_path, 'taskflow.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key-2026'
    
    db.init_app(app)
    
    from app.routes import init_routes
    init_routes(app)
    
    with app.app_context():
        db.create_all()
    
    return app

