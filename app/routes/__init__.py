"""
Módulo de Rutas (Routes) de TaskFlow.

Registra todas las rutas de la aplicación organizadas por dominio.

Estructura:
- auth_routes.py: Login, register, logout
- project_routes.py: CRUD de proyectos
- task_routes.py: CRUD de tareas
"""


def init_routes(app):
    """
    Registra todos los blueprints y rutas en la aplicación.
    
    Args:
        app (Flask): Aplicación Flask
    """
    from app.routes.auth_routes import register_auth_routes
    from app.routes.project_routes import register_project_routes
    from app.routes.task_routes import register_task_routes
    
    # Registrar rutas por dominio
    register_auth_routes(app)
    register_project_routes(app)
    register_task_routes(app)
    
    # Rutas de error
    register_error_routes(app)


def register_error_routes(app):
    """Registra rutas de manejo de errores."""
    from flask import render_template
    
    @app.errorhandler(404)
    def not_found(error):
        """Página no encontrada."""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Error del servidor."""
        return render_template('500.html'), 500