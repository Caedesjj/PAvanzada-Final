"""
Rutas de Proyectos (Project Routes).

Maneja:
- Listar proyectos (dashboard)
- Crear proyecto
- Ver detalles del proyecto
- Editar proyecto
- Eliminar proyecto
"""

from flask import render_template, request, redirect, url_for, session, flash
from app import db
from app.repositories.project_repository import ProjectRepository
from app.models.log_entry import LogEntry


def requires_login(f):
    """Decorador para proteger rutas que requieren autenticación."""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debe iniciar sesión primero', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


def register_project_routes(app):
    """Registra las rutas de proyectos."""
    
    @app.route('/dashboard')
    @requires_login
    def dashboard():
        """
        Dashboard principal.
        
        Muestra todos los proyectos del usuario autenticado.
        """
        user_id = session['user_id']
        projects = ProjectRepository.get_by_owner(user_id)
        
        return render_template('dashboard.html', projects=projects)
    
    @app.route('/project/create', methods=['GET', 'POST'])
    @requires_login
    def create_project():
        """
        Crear nuevo proyecto.
        
        GET: Muestra formulario de creación
        POST: Crea el proyecto en la BD
        """
        if request.method == 'POST':
            name = request.form['name']
            description = request.form.get('description', '')
            user_id = session['user_id']
            
            # Crear proyecto usando repository
            project = ProjectRepository.create(
                name=name,
                description=description,
                owner_id=user_id
            )
            
            # Registrar en log
            log = LogEntry(
                action=LogEntry.ACTION_PROJECT_CREATED,
                description=f"Proyecto '{name}' creado",
                user_id=user_id
            )
            db.session.add(log)
            db.session.commit()
            
            flash('Proyecto creado exitosamente', 'success')
            return redirect(url_for('project_detail', project_id=project.id))
        
        return render_template('create_project.html')
    
    @app.route('/project/<int:project_id>')
    @requires_login
    def project_detail(project_id):
        """
        Ver detalles de un proyecto.
        
        Muestra el proyecto y todas sus tareas.
        
        Args:
            project_id (int): ID del proyecto
        """
        from app.repositories.task_repository import TaskRepository
        
        project = ProjectRepository.get_by_id(project_id)
        
        if not project:
            flash('Proyecto no encontrado', 'error')
            return redirect(url_for('dashboard'))
        
        # Obtener tareas del proyecto
        tasks = TaskRepository.get_by_project(project_id)
        
        return render_template('project_detail.html', project=project, tasks=tasks)
    
    @app.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
    @requires_login
    def edit_project(project_id):
        """
        Editar proyecto.
        
        GET: Muestra formulario de edición
        POST: Actualiza el proyecto
        """
        project = ProjectRepository.get_by_id(project_id)
        
        if not project:
            flash('Proyecto no encontrado', 'error')
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            name = request.form['name']
            description = request.form.get('description', '')
            
            # Actualizar usando repository
            ProjectRepository.update(
                project_id,
                name=name,
                description=description
            )
            
            # Registrar en log
            log = LogEntry(
                action=LogEntry.ACTION_PROJECT_UPDATED,
                description=f"Proyecto '{name}' actualizado",
                user_id=session['user_id']
            )
            db.session.add(log)
            db.session.commit()
            
            flash('Proyecto actualizado', 'success')
            return redirect(url_for('project_detail', project_id=project_id))
        
        return render_template('edit_project.html', project=project)
    
    @app.route('/project/<int:project_id>/delete', methods=['POST'])
    @requires_login
    def delete_project(project_id):
        """
        Eliminar proyecto.
        
        Args:
            project_id (int): ID del proyecto a eliminar
        """
        project = ProjectRepository.get_by_id(project_id)
        
        if not project:
            flash('Proyecto no encontrado', 'error')
            return redirect(url_for('dashboard'))
        
        ProjectRepository.delete(project_id)
        
        # Registrar en log
        log = LogEntry(
            action=LogEntry.ACTION_PROJECT_DELETED,
            description=f"Proyecto '{project.name}' eliminado",
            user_id=session['user_id']
        )
        db.session.add(log)
        db.session.commit()
        
        flash('Proyecto eliminado', 'success')
        return redirect(url_for('dashboard'))
    