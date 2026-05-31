from flask import render_template
from app.models.task import Task
from app.models.project import Project

def init_routes(app):
    
    @app.route('/')
    def index():
        """Controlador: página principal"""
        return render_template('index.html')
    
    @app.route('/tasks')
    def list_tasks():
        """Controlador: listar tareas"""
        tasks = Task.query.all()
        return render_template('tasks.html', tasks=tasks)
    
    @app.route('/projects')
    def list_projects():
        """Controlador: listar proyectos"""
        projects = Project.query.all()
        return render_template('projects.html', projects=projects)