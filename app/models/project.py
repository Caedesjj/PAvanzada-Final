"""
Modelo de Proyecto para TaskFlow.

Este módulo define la clase Project que representa un proyecto donde se
organizan y gestionan tareas colaborativas.

"""

from app import db
from datetime import datetime

"""
    Modelo Project - Representa un proyecto en TaskFlow.
    
    Un proyecto es un contenedor de tareas creado por un usuario (owner).
    Todos los proyectos pueden compartirse con otros miembros del equipo.
    
    Attributes:
        id (int): Identificador único del proyecto (Primary Key).
        name (str): Nombre del proyecto (máx 100 caracteres, requerido).
        description (str): Descripción detallada del proyecto (opcional).
        owner_id (int): ID del usuario propietario (Foreign Key).
        created_at (datetime): Fecha y hora de creación del proyecto.
        updated_at (datetime): Fecha y hora de la última actualización.
        
    Relationships:
        tasks (relationship): Tareas contenidas en este proyecto.
    """

# modelo de proyecto con campos de id, nombre y descripción
class Project(db.Model):

    __tablename__ = "projects"
    
    #Tabla

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    

    # Key al admin del proyecto
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    
    # Relación tablas con Task
    tasks = db.relationship(
        'Task',
        backref='project',  # Permite acceder al proyecto desde Task
        lazy=True,
        cascade='all, delete-orphan'  # Elimina tareas si se elimina proyecto
    )
    
    def __repr__(self):
        """Representación en string del objeto Project."""
        return f'<Project {self.name}>'
    
    def to_dict(self, include_tasks=False):
        """
        Convierte el objeto Project a diccionario.
        
        Args:
            include_tasks (bool): Si incluir la lista de tareas. Default: False.
            
        Returns:
            dict: Diccionario con los atributos del proyecto.
        """
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'task_count': len(self.tasks)
        }
        
        if include_tasks:
            data['tasks'] = [task.to_dict() for task in self.tasks]
        
        return data
    
    

