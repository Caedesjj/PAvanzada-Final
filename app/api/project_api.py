"""
API REST de Proyectos.

Endpoints:
- GET /api/projects - Listar proyectos
- POST /api/projects - Crear proyecto
- GET /api/projects/<id> - Obtener proyecto
- PUT /api/projects/<id> - Actualizar proyecto
- DELETE /api/projects/<id> - Eliminar proyecto
"""

from flask_restful import Resource
from flask import request, session
from app.repositories.project_repository import ProjectRepository


class ProjectListAPI(Resource):
    """API para listar y crear proyectos."""
    
    def get(self):
        """
        GET /api/projects
        
        Retorna lista de proyectos en formato JSON.
        """
        try:
            projects = ProjectRepository.get_all()
            
            return {
                'success': True,
                'count': len(projects),
                'projects': [project.to_dict() for project in projects]
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500
    
    def post(self):
        """
        POST /api/projects
        
        Crea un nuevo proyecto.
        
        Body JSON:
        {
            "name": "Nombre del proyecto",
            "description": "Descripción del proyecto",
            "owner_id": 1
        }
        """
        try:
            data = request.get_json()
            
            if not data.get('name'):
                return {
                    'success': False,
                    'error': 'name es requerido'
                }, 400
            
            project = ProjectRepository.create(
                name=data['name'],
                description=data.get('description', ''),
                owner_id=data.get('owner_id')
            )
            
            return {
                'success': True,
                'message': 'Proyecto creado exitosamente',
                'project': project.to_dict()
            }, 201
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500


class ProjectDetailAPI(Resource):
    """API para obtener, actualizar y eliminar proyectos específicos."""
    
    def get(self, project_id):
        """
        GET /api/projects/<id>
        
        Retorna un proyecto específico con sus tareas.
        """
        try:
            project = ProjectRepository.get_by_id(project_id)
            
            if not project:
                return {
                    'success': False,
                    'error': 'Proyecto no encontrado'
                }, 404
            
            return {
                'success': True,
                'project': project.to_dict(include_tasks=True)
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500
    
    def put(self, project_id):
        """
        PUT /api/projects/<id>
        
        Actualiza un proyecto.
        
        Body JSON:
        {
            "name": "Nuevo nombre",
            "description": "Nueva descripción"
        }
        """
        try:
            project = ProjectRepository.get_by_id(project_id)
            
            if not project:
                return {
                    'success': False,
                    'error': 'Proyecto no encontrado'
                }, 404
            
            data = request.get_json()
            
            updated_project = ProjectRepository.update(project_id, **data)
            
            return {
                'success': True,
                'message': 'Proyecto actualizado exitosamente',
                'project': updated_project.to_dict()
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500
    
    def delete(self, project_id):
        """
        DELETE /api/projects/<id>
        
        Elimina un proyecto.
        """
        try:
            project = ProjectRepository.get_by_id(project_id)
            
            if not project:
                return {
                    'success': False,
                    'error': 'Proyecto no encontrado'
                }, 404
            
            ProjectRepository.delete(project_id)
            
            return {
                'success': True,
                'message': 'Proyecto eliminado exitosamente'
            }, 200
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }, 500