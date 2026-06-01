"""
Inicialización de TaskFlow.
"""

import os
from flask import Flask
from app.models import db


def create_app():
    """Factory de aplicación Flask."""
    app = Flask(__name__, template_folder='templates')
    
    # Asegura que la carpeta instance existe
    os.makedirs(app.instance_path, exist_ok=True)
    
    # ===========================
    # CONFIGURACIÓN DE BD
    # ===========================
    db_path = os.path.join(app.instance_path, 'taskflow.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-2026')
    
    # Inicializar db con la app
    db.init_app(app)
    
    # REGISTRAR RUTAS
   
    from app.routes import init_routes
    init_routes(app)
    

    # REGISTRAR API REST
    
    from app.api import register_api
    register_api(app)
    
    
    # CREAR TABLAS
   
    with app.app_context():
        db.create_all()
        print("✅ Base de datos inicializada")
    
  
    # INICIAR SERVICIOS DE FONDO (PRÓXIMAMENTE)
   
    # TODO: Descomentar después de implementar API REST
    # from app.services import start_background_services
    # start_background_services(app)
    
    return app