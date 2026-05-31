"""
Módulo de Modelos para TaskFlow.

Este paquete contiene todas las clases que representan las tablas de la
base de datos y sus relaciones.
"""

from flask_sqlalchemy import SQLAlchemy

# 1. Crea db ANTES de importar los modelos
db = SQLAlchemy()

# 2. Importar los modelos
from .user import User
from .project import Project
from .task import Task
from .notification import Notification
from .log_entry import LogEntry

# 3. Exportar lo que se necesita
__all__ = [
    'User',
    'Project',
    'Task',
    'Notification',
    'LogEntry',
    'db'
]
