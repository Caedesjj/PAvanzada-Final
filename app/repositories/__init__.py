"""
Módulo de Repositories - Acceso a datos.

Los repositories implementan el patrón Repository,
aislando la lógica de acceso a datos.
"""

from app.repositories.user_repository import UserRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.task_repository import TaskRepository

__all__ = ['UserRepository', 'ProjectRepository', 'TaskRepository']