"""
Servicio de Notificaciones (NotificationService).

HILO 1: Monitorea tareas vencidas cada 60 segundos y crea notificaciones.

Funcionalidad:
- Busca tareas vencidas (due_date < ahora, status != completed)
- Crea notificación automática para el usuario asignado
- Registra en log del sistema
"""

import threading
import time
from datetime import datetime
from app import db
from app.models.task import Task
from app.models.notification import Notification
from app.models.log_entry import LogEntry


class NotificationService:
    """
    Servicio de monitoreo de tareas vencidas.
    
    Ejecuta en un hilo separado (daemon) para no bloquear la app.
    """
    
    def __init__(self, app, check_interval=60):
        """
        Inicializa el servicio.
        
        Args:
            app (Flask): Aplicación Flask
            check_interval (int): Segundos entre revisiones. Default: 60
        """
        self.app = app
        self.check_interval = check_interval
        self.running = True
        self.thread = None
    
    def start(self):
        """Inicia el hilo de monitoreo."""
        self.thread = threading.Thread(
            target=self._monitor_overdue_tasks,
            daemon=True
        )
        self.thread.start()
        print(f" NotificationService iniciado (revisa cada {self.check_interval}s)")
    
    def stop(self):
        """Detiene el hilo de monitoreo."""
        self.running = False
        print(" NotificationService detenido")
    
    def _monitor_overdue_tasks(self):
        """
        Monitorea tareas vencidas continuamente.
        
        - Se ejecuta en un hilo separado
        - Revisa cada 60 segundos
        - Crea notificaciones automáticamente
        """
        while self.running:
            try:
                with self.app.app_context():
                    # Buscar tareas vencidas
                    overdue_tasks = Task.query.filter(
                        Task.status != 'completed',
                        Task.due_date < datetime.utcnow()
                    ).all()
                    
                    for task in overdue_tasks:
                        # Verificar si ya existe notificación para esta tarea
                        existing_notification = Notification.query.filter_by(
                            task_id=task.id,
                            message__like=f"%{task.title}%vencida%"
                        ).first()
                        
                        # Si no existe y tiene usuario asignado, crear notificación
                        if not existing_notification and task.assigned_to:
                            notification = Notification(
                                message=f"⚠️ Tarea '{task.title}' está VENCIDA",
                                read=False,
                                user_id=task.assigned_to,
                                task_id=task.id
                            )
                            db.session.add(notification)
                            
                            # Registrar en log
                            log = LogEntry(
                                action=LogEntry.ACTION_NOTIFICATION_CREATED,
                                description=f"Notificación de tarea vencida: '{task.title}'",
                                user_id=task.assigned_to
                            )
                            db.session.add(log)
                    
                    db.session.commit()
                    
                    if overdue_tasks:
                        print(f" Se detectaron {len(overdue_tasks)} tareas vencidas")
                
                # Esperar 60 segundos antes de revisar nuevamente
                time.sleep(self.check_interval)
            
            except Exception as e:
                print(f" Error en NotificationService: {e}")
                # Registrar error
                try:
                    with self.app.app_context():
                        log = LogEntry(
                            action=LogEntry.ACTION_ERROR,
                            description=f"Error en NotificationService: {str(e)}"
                        )
                        db.session.add(log)
                        db.session.commit()
                except:
                    pass
                
                # Continuar ejecutándose
                time.sleep(self.check_interval)