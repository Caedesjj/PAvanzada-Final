from app.models import db
from datetime import datetime

"""
Modelo de Notificación para TaskFlow.

Este módulo define la clase Notification que representa alertas y notificaciones
en el sistema, generadas automáticamente por eventos (tareas vencidas, etc).

"""
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    
    # Foreign Keys
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )
    task_id = db.Column(
        db.Integer,
        db.ForeignKey('tasks.id'),
        nullable=True
    )
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """Representación en string del objeto Notification."""
        return f'<Notification {self.id} - {"Leída" if self.read else "Sin leer"}>'
    
    def mark_as_read(self):
        """Marca la notificación como leída."""
        self.read = True
        db.session.commit()
    
    def to_dict(self):
        """
        Convierte el objeto Notification a diccionario.
        
        Returns:
            dict: Diccionario con los atributos de la notificación.
        """
        return {
            'id': self.id,
            'message': self.message,
            'read': self.read,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

