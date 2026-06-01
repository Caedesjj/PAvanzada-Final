"""
Módulo de Servicios de TaskFlow.

Contiene la lógica de negocio y procesos concurrentes (hilos).

Servicios:
- NotificationService: Monitorea tareas vencidas
- LogService: Escribe logs en archivo
"""

from app.services.notification_service import NotificationService
from app.services.log_service import LogService

__all__ = ['NotificationService', 'LogService', 'start_background_services']


def start_background_services(app):
    """
    Inicia los servicios de fondo (hilos).
    
    Debe ser llamado desde app/__init__.py después de crear la app.
    
    Args:
        app (Flask): Aplicación Flask
    """
    notification_service = NotificationService(app)
    log_service = LogService(app)
    
    notification_service.start()
    log_service.start()
    
    return notification_service, log_service