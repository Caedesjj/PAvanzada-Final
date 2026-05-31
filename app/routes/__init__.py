from flask import render_template

def init_routes(app):
    """Registra todas las rutas de la aplicación."""
       
    # Registrar rutas de autenticación (login, register, logout, index)
    from app.routes.auth_routes import register_auth_routes
    register_auth_routes(app)   # Esta función ya define '/' y '/login', '/register', etc.
    
    # Registrar rutas de proyectos
    from app.routes.project_routes import register_project_routes
    register_project_routes(app)
    
    # Registrar rutas de tareas
    from app.routes.task_routes import register_task_routes
    register_task_routes(app)
    
    # Manejo de errores (opcional)
    register_error_routes(app)


def register_error_routes(app):
    from flask import render_template
    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404
    @app.errorhandler(500)
    def server_error(error):
        return render_template('500.html'), 500