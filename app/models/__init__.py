

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

"""
Módulo de Modelos para TaskFlow.

Este paquete contiene todas las clases que representan las tablas de la
base de datos y sus relaciones.

Clases:
    - User: Usuarios del sistema
    - Project: Proyectos colaborativos
    - Task: Tareas dentro de un proyecto
    - Notification: Notificaciones automáticas
    - LogEntry: Registro de auditoría del sistema
    
"""

from .user import User
from .project import Project
from .task import Task
from .notification import Notification
from .log_entry import LogEntry

__all__ = [
    'User',
    'Project',
    'Task',
    'Notification',
    'LogEntry',
    'db'
]



db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/taskflow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-key'
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app