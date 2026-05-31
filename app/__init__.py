import os
from flask import Flask
from app.models import db   # importa db desde models

def create_app():
    app = Flask(__name__, template_folder='templates')
    
    # Asegura que la carpeta instance existe
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Configurar base de datos
    db_path = os.path.join(app.instance_path, 'taskflow.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-2026')
    
    # Inicializar db con la app
    db.init_app(app)
    
    # Registrar rutas (blueprints)
    from app.routes import init_routes
    init_routes(app)
    
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    
    return app