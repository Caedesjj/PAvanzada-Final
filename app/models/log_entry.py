from app import db
from datetime import datetime

  # Tipos de acciones válidas en el sistema
ACTION_USER_LOGIN = "user_login"
ACTION_USER_LOGOUT = "user_logout"
ACTION_USER_CREATED = "user_created"
ACTION_PROJECT_CREATED = "project_created"
ACTION_PROJECT_UPDATED = "project_updated"
ACTION_PROJECT_DELETED = "project_deleted"
ACTION_TASK_CREATED = "task_created"
ACTION_TASK_UPDATED = "task_updated"
ACTION_TASK_DELETED = "task_deleted"
ACTION_TASK_COMPLETED = "task_completed"
ACTION_NOTIFICATION_CREATED = "notification_created"
ACTION_ERROR = "error"

class LogEntry(db.Model):

    """
    Modelo LogEntry - Representa un registro de actividad en TaskFlow.
    
    Se registran todas las acciones del sistema:
    - Creación, edición, eliminación de recursos
    - Inicios y cierres de sesión
    - Cambios de estado
    - Errores importantes
    
    Attributes:
        id (int): Identificador único del registro (Primary Key).
        action (str): Tipo de acción realizada (máx 100 caracteres).
                      Ej: 'user_login', 'task_created', 'project_deleted'
        description (str): Descripción detallada de la acción (opcional).
        user_id (int): ID del usuario que realizó la acción (Foreign Key, opcional).
        created_at (datetime): Fecha y hora en que ocurrió la acción.
    """
    
    __tablename__ = "log_entries"

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """Representación en string del objeto LogEntry."""
        return f'<LogEntry {self.action} by User {self.user_id} at {self.created_at}>'
    
    
    def to_dict(self):
        """
        Convierte el objeto LogEntry a diccionario.
        
        Returns:
            dict: Diccionario con los atributos del registro de actividad.
        """
        return {
            'id': self.id,
            'action': self.action,
            'description': self.description,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        