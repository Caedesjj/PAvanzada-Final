"""
Rutas de Tareas (Task Routes).

Maneja:
- Crear tarea
- Actualizar estado de tarea
- Eliminar tarea
"""

from flask import request, redirect, url_for, session, flash, render_template
from app import db
from app.repositories.task_repository import TaskRepository
from app.repositories.project_repository import ProjectRepository
from app.models.log_entry import LogEntry
from datetime import datetime


def requires_login(f):
    """Decorador para proteger rutas que requieren autenticación."""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debe iniciar sesión primero', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


def register_task_routes(app):
    """Registra las rutas de tareas."""
    
    @app.route('/task/create/<int:project_id>', methods=['GET', 'POST'])
    @requires_login
    def create_task(project_id):
        """
        Crear nueva tarea.
        
        GET: Muestra formulario de creación
        POST: Crea la tarea en la BD
        
        Args:
            project_id (int): ID del proyecto donde crear la tarea
        """
        project = ProjectRepository.get_by_id(project_id)
        
        if not project:
            flash('Proyecto no encontrado', 'error')
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            title = request.form['title']
            description = request.form.get('description', '')
            priority = request.form.get('priority', 'medium')
            due_date_str = request.form.get('due_date')
            assigned_to = request.form.get('assigned_to') or None
            
            # Convertir due_date
            due_date = None
            if due_date_str:
                try:
                    due_date = datetime.fromisoformat(due_date_str)
                except:
                    pass
            
            # Crear tarea usando repository
            task = TaskRepository.create(
                title=title,
                project_id=project_id,
                description=description,
                priority=priority,
                due_date=due_date,
                assigned_to=assigned_to
            )
            
            # Registrar en log
            log = LogEntry(
                action=LogEntry.ACTION_TASK_CREATED,
                description=f"Tarea '{title}' creada en proyecto '{project.name}'",
                user_id=session['user_id']
            )
            db.session.add(log)
            db.session.commit()
            
            flash('Tarea creada exitosamente', 'success')
            return redirect(url_for('project_detail', project_id=project_id))
        
        return render_template('create_task.html', project=project)
    
    @app.route('/task/<int:task_id>/update', methods=['POST'])
    @requires_login
    def update_task(task_id):
        """
        Actualizar estado de tarea.
        
        Actualiza el estado (pending, in_progress, completed) y prioridad.
        
        Args:
            task_id (int): ID de la tarea a actualizar
        """
        task = TaskRepository.get_by_id(task_id)
        
        if not task:
            flash('Tarea no encontrada', 'error')
            return redirect(url_for('dashboard'))
        
        status = request.form.get('status')
        priority = request.form.get('priority')
        
        # Actualizar usando repository
        TaskRepository.update(
            task_id,
            status=status,
            priority=priority
        )
        
        # Registrar en log
        log = LogEntry(
            action=LogEntry.ACTION_TASK_UPDATED,
            description=f"Tarea '{task.title}' actualizada - Status: {status}",
            user_id=session['user_id']
        )
        db.session.add(log)
        db.session.commit()
        
        flash('Tarea actualizada', 'success')
        return redirect(url_for('project_detail', project_id=task.project_id))
    
    @app.route('/task/<int:task_id>/delete', methods=['POST'])
    @requires_login
    def delete_task(task_id):
        """
        Eliminar tarea.
        
        Args:
            task_id (int): ID de la tarea a eliminar
        """
        task = TaskRepository.get_by_id(task_id)
        
        if not task:
            flash('Tarea no encontrada', 'error')
            return redirect(url_for('dashboard'))
        
        project_id = task.project_id
        task_title = task.title
        
        TaskRepository.delete(task_id)
        
        # Registrar en log
        log = LogEntry(
            action=LogEntry.ACTION_TASK_DELETED,
            description=f"Tarea '{task_title}' eliminada",
            user_id=session['user_id']
        )
        db.session.add(log)
        db.session.commit()
        
        flash('Tarea eliminada', 'success')
        return redirect(url_for('project_detail', project_id=project_id))