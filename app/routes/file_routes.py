"""Rutas para manejo de archivos."""

import os
from flask import request, send_file, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from app import db
from app.repositories.task_repository import TaskRepository

# Carpeta de uploads en la raíz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'data', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'jpg', 'png', 'zip'}

# Crear carpeta si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
print(f"✅ Carpeta de uploads creada: {UPLOAD_FOLDER}")


def allowed_file(filename):
    """Verifica si la extensión es permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def register_file_routes(app):
    """Registra rutas de manejo de archivos."""
    
    @app.route('/task/<int:task_id>/upload', methods=['POST'])
    def upload_file(task_id):
        """Sube un archivo a una tarea."""
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        task = TaskRepository.get_by_id(task_id)
        if not task:
            flash('Tarea no encontrada', 'error')
            return redirect(url_for('dashboard'))
        
        if 'file' not in request.files:
            flash('No se seleccionó archivo', 'error')
            return redirect(url_for('project_detail', project_id=task.project_id))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No se seleccionó archivo', 'error')
            return redirect(url_for('project_detail', project_id=task.project_id))
        
        if not allowed_file(file.filename):
            flash('Tipo de archivo no permitido', 'error')
            return redirect(url_for('project_detail', project_id=task.project_id))
        
        try:
            filename = secure_filename(file.filename)
            unique_filename = f"task_{task_id}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            
            # Eliminar archivo anterior si existe
            if task.document_path and os.path.exists(task.document_path):
                try:
                    os.remove(task.document_path)
                except:
                    pass
            
            # Guardar archivo
            file.save(filepath)
            
            # Guardar en BD (guardar ruta relativa para compatibilidad)
            task.document_filename = filename
            task.document_path = filepath  # Ruta completa
            db.session.commit()
            
            flash(f'✅ Archivo "{filename}" subido', 'success')
            print(f"✅ Archivo guardado: {filepath}")
        
        except Exception as e:
            flash(f'❌ Error: {str(e)}', 'error')
            print(f"❌ Error subiendo: {e}")
        
        return redirect(url_for('project_detail', project_id=task.project_id))
    
    @app.route('/task/<int:task_id>/download')
    def download_file(task_id):
        """Descarga archivo de una tarea."""
        task = TaskRepository.get_by_id(task_id)
        
        if not task or not task.document_path:
            flash('Archivo no encontrado', 'error')
            return redirect(url_for('dashboard'))
        
        try:
            filepath = task.document_path
            
            # Verificar que existe
            if not os.path.exists(filepath):
                flash('El archivo no existe', 'error')
                print(f"❌ No existe: {filepath}")
                return redirect(url_for('dashboard'))
            
            print(f"✅ Descargando: {filepath}")
            return send_file(
                filepath,
                as_attachment=True,
                download_name=task.document_filename
            )
        
        except Exception as e:
            flash('Error al descargar', 'error')
            print(f"❌ Error: {e}")
            return redirect(url_for('dashboard'))