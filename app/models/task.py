from app import db
from datetime import datetime

"""
Crear tareas dentro de un proyecto con nombre, descripción, 
prioridad y fecha límite."

"Asignar una tarea a un miembro del equipo."

"Un hilo en segundo plano revisa si hay tareas VENCIDAS 
y genera alertas para el usuario asignado y el propietario del proyecto.


"""
class Task(db.Model):
    
    """
    Modelo Task - Representa una tarea en TaskFlow.
    
    Las tareas pertenecen a un proyecto específico y pueden asignarse a
    miembros del equipo. Tienen estados (pending, in_progress, completed),
    prioridades (low, medium, high) y fechas límite.
    
    Attributes:
        id (int): Identificador único de la tarea (Primary Key).
        title (str): Título/nombre de la tarea (máx 100 caracteres).
        description (str): Descripción detallada de la tarea (opcional).
        priority (str): Nivel de prioridad ('low', 'medium', 'high'). Default: 'medium'.
        status (str): Estado de la tarea ('pending', 'in_progress', 'completed'). Default: 'pending'.
        due_date (datetime): Fecha límite de vencimiento (opcional).
        project_id (int): ID del proyecto al que pertenece (Foreign Key).
        assigned_to (int): ID del usuario responsable (Foreign Key, opcional).
        created_at (datetime): Fecha y hora de creación de la tarea.
        updated_at (datetime): Fecha y hora de la última actualización.
        
    Relationships:
        notifications (relationship): Notificaciones relacionadas con esta tarea.
    """
    
    __tablename__ = "tasks"
    
    # Estados válidos para una tarea
    STATUS_PENDING = "pendiente"
    STATUS_IN_PROGRESS = "en_progreso"
    STATUS_COMPLETED = "completada"
    VALID_STATUSES = [STATUS_PENDING, STATUS_IN_PROGRESS, STATUS_COMPLETED]
    
    # Prioridades válidas
    PRIORITY_LOW = "baja"
    PRIORITY_MEDIUM = "media"
    PRIORITY_HIGH = "alta"
    VALID_PRIORITIES = [PRIORITY_LOW, PRIORITY_MEDIUM, PRIORITY_HIGH]
    
    # Atributos de la tabla
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(
        db.String(20),
        default=PRIORITY_MEDIUM,
        nullable=False
    )
    status = db.Column(
        db.String(20),
        default=STATUS_PENDING,
        nullable=False
    )
    due_date = db.Column(db.DateTime, nullable=True)
    
    # Foreign Keys
    project_id = db.Column(
        db.Integer,
        db.ForeignKey('projects.id'),
        nullable=False
    )
    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=True
    )
    
    # Timestamps para auditoría
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relación One-to-Many con Notification
    notifications = db.relationship(
        'Notification',
        backref='task',
        lazy=True,
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        """Representación en string del objeto Task."""
        return f'<Task {self.title} [{self.status}]>'
    
    def is_overdue(self):
        """
        Verifica si la tarea está vencida.
        
        Returns:
            bool: True si la tarea está vencida y no está completada.
        """
        if self.status == self.STATUS_COMPLETED:
            return False
        
        if self.due_date is None:
            return False
        
        return datetime.utcnow() > self.due_date
    
    def to_dict(self, include_assignee=False):
        """
        Convierte el objeto Task a diccionario.
        
        Args:
            include_assignee (bool): Si incluir datos del usuario asignado. Default: False.
            
        Returns:
            dict: Diccionario con los atributos de la tarea.
        """
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'project_id': self.project_id,
            'assigned_to': self.assigned_to,
            'is_overdue': self.is_overdue(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_assignee and self.assigned_user:
            data['assignee'] = self.assigned_user.to_dict()
        
        return data

