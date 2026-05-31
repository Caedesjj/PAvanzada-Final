from flask import render_template

def init_routes(app):
    """Registra todas las rutas de la aplicación."""
    
    @app.route('/')
    def index():
        return render_template('index.html')