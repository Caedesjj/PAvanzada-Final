"""
Módulo de API REST de TaskFlow.

Endpoints JSON para consumir desde clientes externos.

APIs:
- TaskAPI: CRUD de tareas
- ProjectAPI: CRUD de proyectos
"""

from flask_restful import Api

api = Api()


def register_api(app):
    """Registra todos los endpoints de la API."""
    from app.api.task_api import TaskListAPI, TaskDetailAPI
    from app.api.project_api import ProjectListAPI, ProjectDetailAPI
    
    # Inicializar API con la app
    api.init_app(app)
    

    # ENDPOINTS DE TAREAS
    
    api.add_resource(
        TaskListAPI,
        '/api/projects/<int:project_id>/tasks',
        '/api/tasks'
    )
    
    api.add_resource(
        TaskDetailAPI,
        '/api/tasks/<int:task_id>'
    )
    
    # ENDPOINTS DE PROYECTOS
   
    api.add_resource(
        ProjectListAPI,
        '/api/projects'
    )
    
    api.add_resource(
        ProjectDetailAPI,
        '/api/projects/<int:project_id>'
    )
