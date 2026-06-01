"""
Servicio de Logs (LogService).

HILO 2: Escribe logs del sistema en un archivo cada 30 segundos.

Funcionalidad:
- Lee logs de la BD
- Los escribe en un archivo CSV/TXT
- Mantiene un archivo de auditoría del sistema
"""

import threading
import time
import csv
from datetime import datetime
from app import db
from app.models.log_entry import LogEntry


class LogService:
    """
    Servicio de escritura de logs en archivo.
    
    Ejecuta en un hilo separado (daemon) para no bloquear la app.
    """
    
    def __init__(self, app, log_file='data/output/system_audit.csv', write_interval=30):
        """
        Inicializa el servicio.
        
        Args:
            app (Flask): Aplicación Flask
            log_file (str): Ruta del archivo de logs. Default: 'data/output/system_audit.csv'
            write_interval (int): Segundos entre escrituras. Default: 30
        """
        self.app = app
        self.log_file = log_file
        self.write_interval = write_interval
        self.running = True
        self.thread = None
        self.last_log_id = 0  # Para rastrear logs ya escritos
    
    def start(self):
        """Inicia el hilo de escritura de logs."""
        # Crear archivo si no existe
        self._init_log_file()
        
        self.thread = threading.Thread(
            target=self._write_logs,
            daemon=True
        )
        self.thread.start()
        print(f" LogService iniciado (escribe cada {self.write_interval}s a {self.log_file})")
    
    def stop(self):
        """Detiene el hilo de escritura de logs."""
        self.running = False
        print(" LogService detenido")
    
    def _init_log_file(self):
        """Crea el archivo de logs si no existe."""
        import os
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Crear archivo con encabezados si no existe
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'TIMESTAMP', 'ACTION', 'DESCRIPTION', 'USER_ID'])
            print(f" Archivo de logs creado: {self.log_file}")
    
    def _write_logs(self):
        """
        Escribe logs continuamente en archivo.
        
        - Se ejecuta en un hilo separado
        - Escribe cada 30 segundos
        - Formato: CSV para fácil análisis
        """
        while self.running:
            try:
                with self.app.app_context():
                    # Obtener logs nuevos desde la última ID
                    new_logs = LogEntry.query.filter(
                        LogEntry.id > self.last_log_id
                    ).order_by(LogEntry.id.asc()).all()
                    
                    if new_logs:
                        # Escribir logs en archivo
                        with open(self.log_file, 'a', newline='') as f:
                            writer = csv.writer(f)
                            for log in new_logs:
                                writer.writerow([
                                    log.id,
                                    log.created_at.isoformat() if log.created_at else '',
                                    log.action,
                                    log.description or '',
                                    log.user_id or ''
                                ])
                        
                        # Actualizar último ID procesado
                        self.last_log_id = new_logs[-1].id
                        print(f" {len(new_logs)} logs escritos al archivo")
                
                # Esperar 30 segundos antes de escribir nuevamente
                time.sleep(self.write_interval)
            
            except Exception as e:
                print(f" Error en LogService: {e}")
                # Continuar ejecutándose
                time.sleep(self.write_interval)