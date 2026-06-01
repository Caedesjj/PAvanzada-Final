"""
API REST de Tareas.

Endpoints:
- GET /api/tasks - Listar todas las tareas
- GET /api/projects/<id>/tasks - Listar tareas de un proyecto
- POST /api/projects/<id>/tasks - Crear tarea
- GET /api/tasks/<id> - Obtener tarea
- PUT /api/tasks/<id> - Actualizar tarea
- DELETE /api/tasks/<id> - Eliminar tarea
"""

from flask_restful import Resource, reqparse
from flask import request
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from datetime import datetime


class TaskListAPI(Resource):
    """API para listar y crear tareas."""
    
    def get(self, project_id=None):
        """
        GET /api/tasks o GET /api/projects/<id>/tasks
        
        Retorna lista de tareas en formato JSON.
        """
        try:
            if project_id:
                # Tareas de un proyecto específico
                tasks = TaskRepository.get_by_project(project_id)
            else:
                # Todas las tareas
                tasks = TaskRepository.get_all()
            
            return {
                'success': True,
                'count': len(tasks),
                'tasks': [task.to_dict() for task in tasks]
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500
    
    def post(self, project_id=None):
        """
        POST /api/projects/<id>/tasks
        
        Crea una nueva tarea.
        
        Body JSON:
        {
            "title": "Nombre de tarea",
            "description": "Descripción",
            "priority": "high|medium|low",
            "due_date": "2026-05-31T18:00:00"
        }
        """
        try:
            data = request.get_json()
            
            if not project_id:
                return {'success': False, 'error': 'project_id requerido'}, 400
            
            # Verificar que el proyecto existe
            project = ProjectRepository.get_by_id(project_id)
            if not project:
                return {'success': False, 'error': 'Proyecto no encontrado'}, 404
            
            # Crear tarea
            task = TaskRepository.create(
                title=data.get('title'),
                project_id=project_id,
                description=data.get('description', ''),
                priority=data.get('priority', 'medium'),
                due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
                assigned_to=data.get('assigned_to')
            )
            
            return {
                'success': True,
                'message': 'Tarea creada exitosamente',
                'task': task.to_dict()
            }, 201
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500


class TaskDetailAPI(Resource):
    """API para obtener, actualizar y eliminar tareas específicas."""
    
    def get(self, task_id):
        """
        GET /api/tasks/<id>
        
        Retorna una tarea específica.
        """
        try:
            task = TaskRepository.get_by_id(task_id)
            
            if not task:
                return {
                    'success': False,
                    'error': 'Tarea no encontrada'
                }, 404
            
            return {
                'success': True,
                'task': task.to_dict(include_assignee=True)
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500
    
    def put(self, task_id):
        """
        PUT /api/tasks/<id>
        
        Actualiza una tarea.
        
        Body JSON:
        {
            "title": "Nuevo título",
            "status": "pending|in_progress|completed",
            "priority": "high|medium|low",
            "description": "Nueva descripción"
        }
        """
        try:
            task = TaskRepository.get_by_id(task_id)
            
            if not task:
                return {
                    'success': False,
                    'error': 'Tarea no encontrada'
                }, 404
            
            data = request.get_json()
            
            # Actualizar tarea
            updated_task = TaskRepository.update(task_id, **data)
            
            return {
                'success': True,
                'message': 'Tarea actualizada exitosamente',
                'task': updated_task.to_dict()
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500
    
    def delete(self, task_id):
        """
        DELETE /api/tasks/<id>
        
        Elimina una tarea.
        """
        try:
            task = TaskRepository.get_by_id(task_id)
            
            if not task:
                return {
                    'success': False,
                    'error': 'Tarea no encontrada'
                }, 404
            
            TaskRepository.delete(task_id)
            
            return {
                'success': True,
                'message': 'Tarea eliminada exitosamente'
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500