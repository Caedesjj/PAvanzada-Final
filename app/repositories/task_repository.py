"""Repository de Tarea."""

from app import db
from app.models.task import Task
from datetime import datetime


class TaskRepository:
    """Repositorio para operaciones CRUD de Task."""
    
    @staticmethod
    def create(title, project_id, description=None, priority='medium', 
               due_date=None, assigned_to=None):
        """
        Crea una nueva tarea.
        
        Args:
            title (str): Título de la tarea
            project_id (int): ID del proyecto
            description (str): Descripción
            priority (str): Prioridad (low, medium, high)
            due_date (datetime): Fecha límite
            assigned_to (int): ID del usuario asignado
        
        Returns:
            Task: Tarea creada
        """
        task = Task(
            title=title,
            project_id=project_id,
            description=description,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to
        )
        
        db.session.add(task)
        db.session.commit()
        
        return task
    
    @staticmethod
    def get_by_id(task_id):
        """Obtiene una tarea por ID."""
        return Task.query.get(task_id)
    
    @staticmethod
    def get_by_project(project_id):
        """
        Obtiene todas las tareas de un proyecto.
        
        Args:
            project_id (int): ID del proyecto
        
        Returns:
            list: Lista de tareas
        """
        return Task.query.filter_by(project_id=project_id).all()
    
    @staticmethod
    def get_by_assignee(user_id):
        """
        Obtiene todas las tareas asignadas a un usuario.
        
        Args:
            user_id (int): ID del usuario
        
        Returns:
            list: Lista de tareas
        """
        return Task.query.filter_by(assigned_to=user_id).all()
    
    @staticmethod
    def get_overdue():
        """
        Obtiene todas las tareas vencidas (no completadas y fecha < ahora).
        
        Returns:
            list: Lista de tareas vencidas
        """
        return Task.query.filter(
            Task.status != 'completed',
            Task.due_date < datetime.utcnow()
        ).all()
    
    @staticmethod
    def get_all():
        """Obtiene todas las tareas."""
        return Task.query.all()
    
    @staticmethod
    def update(task_id, **kwargs):
        """
        Actualiza una tarea.
        
        Args:
            task_id (int): ID de la tarea
            **kwargs: Campos a actualizar
        
        Returns:
            Task: Tarea actualizada o None
        """
        task = Task.query.get(task_id)
        
        if not task:
            return None
        
        if 'title' in kwargs:
            task.title = kwargs['title']
        if 'description' in kwargs:
            task.description = kwargs['description']
        if 'priority' in kwargs:
            task.priority = kwargs['priority']
        if 'status' in kwargs:
            task.status = kwargs['status']
        if 'due_date' in kwargs:
            task.due_date = kwargs['due_date']
        if 'assigned_to' in kwargs:
            task.assigned_to = kwargs['assigned_to']
        
        db.session.commit()
        return task
    
    @staticmethod
    def delete(task_id):
        """Elimina una tarea."""
        task = Task.query.get(task_id)
        
        if not task:
            return False
        
        db.session.delete(task)
        db.session.commit()
        return True
    