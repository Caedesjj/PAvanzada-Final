
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
