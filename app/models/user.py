"""
Modelo de Usuario para TaskFlow.

Define la clase User que representa a los usuarios del sistema.
Los usuarios pueden tener roles (admin, member) y crear proyectos.

"""


from app.models import db
from datetime import datetime



# modelo de usuario con campos de id, nombre, email, contraseña y rol
class User(db.Model):
    
    """
    Modelo User - Representa un usuario del sistema.
    
    Attributos:
        id (int): Identificador único del usuario (Primary Key).
        name (str): Nombre completo del usuario (máx 100 caracteres).
        email (str): Email único del usuario (máx 120 caracteres).
        username (str): Nombre de usuario único para login (máx 80 caracteres).
        password (str): Contraseña hasheada del usuario (máx 255 caracteres).
        role (str): Rol del usuario ('admin' o 'member'). Default: 'member'.
        created_at (datetime): Fecha y hora de creación del registro.
        updated_at (datetime): Fecha y hora de la última actualización.
        
    Relaciones:
        projects: Proyectos creados por este usuario.
        tasks: Tareas asignadas a este usuario.
        notifications: Notificaciones del usuario.
        log_entries: Registro de actividades del usuario.
    """

    __tablename__ = "users"
    
    #Atributos de tabla

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="member")
    
# Relaciones con otras tablas
    projects = db.relationship(
        'Project',
        backref='owner',  # Permite acceder al propietario desde Project
        lazy=True,
        cascade='all, delete-orphan'  # Elimina proyectos si se elimina usuario
    )
    
    tasks = db.relationship(
        'Task',
        backref='assigned_user',  # Permite acceder al usuario asignado desde Task
        lazy=True,
        foreign_keys='Task.assigned_to'  # Especifica cuál usar
    )
    
    notifications = db.relationship(
        'Notification',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    log_entries = db.relationship(
        'LogEntry',
        backref='user',
        lazy=True
    )
    
    def __repr__(self):
        """Representación en string del objeto User."""
        return f'<User {self.username}>'
    
    def to_dict(self):
        """
        Convierte el objeto User a diccionario.
        
        Returns:
            dict: Diccionario con los atributos del usuario.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
