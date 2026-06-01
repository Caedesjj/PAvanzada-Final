## Público objetivo

TaskFlow está dirigido principalmente a:

- Equipos de trabajo pequeños y medianos.
- Grupos de desarrollo de software.
- Equipos académicos que realizan proyectos colaborativos.
- Organizaciones que necesitan seguimiento de tareas y proyectos.
- Administradores que requieren supervisar actividades y auditorías del sistema.

También puede ser utilizado por desarrolladores externos gracias a su API REST, 
permitiendo integraciones con otras aplicaciones y servicios.

## ¿Qué ofrece TaskFlow?

TaskFlow proporciona una plataforma centralizada para gestionar proyectos y tareas mediante:

- Gestión de usuarios
- Autenticación y autorización.
- Roles diferenciados (administrador y miembro).
- Control de acceso a los recursos.
- Gestión de proyectos
- Creación y organización de proyectos.
- Asignación de propietarios.
- Agrupación de tareas dentro de cada proyecto.
- Gestión de tareas
- Creación, edición y seguimiento de tareas.
- Estados de avance (pendiente, completada, etc.).
- Priorización de actividades.
- Adjuntos y documentación asociada.
- Sistema de notificaciones
- Alertas automáticas para tareas vencidas.
- Seguimiento de fechas límite.
- Comunicación de eventos relevantes.
- Auditoría y trazabilidad
- Registro de acciones realizadas por los usuarios.
- Historial de eventos del sistema.
- Soporte para monitoreo y análisis de actividad.
- Acceso dual
- Interfaz web amigable basada en Flask y Jinja2.
- API REST para integración con aplicaciones externas.
## ¿Por qué es una buena solución?
### 1. Centraliza la gestión del trabajo

En lugar de depender de múltiples herramientas dispersas (hojas de cálculo, correos, mensajes, etc.), 
TaskFlow concentra toda la información en un único sistema.

### 2. Facilita el trabajo colaborativo

La estructura Usuario → Proyecto → Tarea permite coordinar equipos de manera organizada y mantener 
visibilidad sobre el progreso de cada actividad.

### 3. Reduce el riesgo de olvidos

El sistema de notificaciones automatizadas ayuda a detectar tareas vencidas y plazos próximos, disminuyendo retrasos en los proyectos.

### 4. Mejora la trazabilidad

Gracias a los registros de auditoría, es posible conocer qué acciones se realizaron, cuándo 
ocurrieron y quién las ejecutó.

### 5. Arquitectura escalable y mantenible

El uso de:

- Flask
- SQLAlchemy
- Repository Pattern
- API REST
- Flask-Migrate

permite que el sistema pueda crecer sin necesidad de rediseñar completamente su estructura.

### 6. Reutilización e integración

La API REST hace posible conectar TaskFlow con aplicaciones móviles, dashboards externos o herramientas empresariales, ampliando sus posibilidades de uso.



## INFORME TÉCNICO: ARQUITECTURA Y DESARROLLO DE TASKFLOW
### 1. Introducción y Propósito del Sistema

TaskFlow es una aplicación web de gestión de proyectos y tareas colaborativas orientada a entornos de 
desarrollo ágil. El sistema centraliza el ciclo de vida de un proyecto —desde su creación y asignación de usuarios 
responsables hasta la ejecución y culminación de subtareas individuales— proveyendo además un sistema 
automatizado de auditoría y notificaciones.

El propósito de este informe es documentar la especificación arquitectónica del software, detallando la 
segregación de responsabilidades, los mecanismos de persistencia de datos, el uso de programación 
concurrente en segundo plano y el patrón de diseño estructural que rige la aplicación.

### 2. Estructura de Directorios del Proyecto

El sistema adopta una estructura modular que separa la lógica de negocio, la capa de persistencia, las interfaces de usuario (HTML/Jinja2) y los servicios asíncronos.
Plaintext

    taskflow/
    │
    ├── app/                        # Paquete principal de la aplicación
    │   ├── __init__.py             # Inicialización (Application Factory y Extensiones)
    │   ├── config.py               # Configuración del entorno y variables del sistema
    │   │
    │   ├── models/                 # Capa de Modelos (Dominio / ORM SQLAlchemy)
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── project.py
    │   │   ├── task.py
    │   │   ├── notification.py
    │   │   └── log_entry.py
    │   │
    │   ├── repositories/           # Capa de Acceso a Datos (Patrón Repository)
    │   │   ├── user_repository.py
    │   │   ├── project_repository.py
    │   │   └── task_repository.py
    │   │
    │   └── rutas/                  # Capa de Controladores (Rutas Flask Web y REST API)
    │       ├── auth_routes.py
    │       ├── project_routes.py
    │       ├── task_routes.py
    │       ├── file_routes.py
    │       └── project_api.py & task_api.py (Flask-RESTful)
    │
    ├── data/                       # Almacenamiento local persistente
    │   ├── taskflow.db             # Base de datos relacional SQLite
    │   ├── output/                 # Archivos generados (system_audit.csv)
    │   └── uploads/                # Documentos adjuntos subidos por usuarios
    │
    ├── migrations/                 # Scripts de evolución del esquema (Flask-Migrate)
    └── run.py                      # Punto de entrada para el servidor Localhost

### 3. Arquitectura y Patrón de Diseño

TaskFlow implementa una variante robusta del patrón MVC (Model-View-Controller) combinada con el patrón Repository, lo que permite una estricta separación de responsabilidades (Separation of Concerns).

    Modelo (Models): Las clases de dominio (User, Project, Task, etc.) representan las 
    entidades del mundo real y las reglas de datos en la base de datos a través de SQLAlchemy.

    Repositorios (Repositories): Actúan como una capa de abstracción intermedia entre los 
    modelos y el controlador. Encapsulan las consultas complejas de SQLAlchemy (operaciones CRUD).
    Esto evita que la lógica de acceso a datos se "filtre" hacia las rutas.

    Controlador/Rutas (Routes & APIs): Reciben las peticiones HTTP (GET, POST, PUT, DELETE), 
    extraen los datos del formulario o JSON, invocan los métodos estáticos del repositorio
    pertinente y redirigen al usuario o retornan una respuesta estructurada.

    Vista (Templates): Representada por los archivos HTML renderizados dinámicamente en 
    el servidor mediante el motor de plantillas Jinja2 (como dashboard.html o project_detail.html), 
    consumiendo los diccionarios de datos enviados por las rutas.

El Patrón Application Factory

Para evitar dependencias circulares y permitir configuraciones dinámicas, el núcleo del framework no inicializa la aplicación globalmente. En su lugar, en app/__init__.py se implementa la función de fábrica:
Python

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    # Registro de rutas y servicios...
    return app

### 4. Persistencia de Datos y Evolución del Esquema
Mecanismo de Persistencia

El sistema utiliza una base de datos relacional local SQLite configurada bajo la URI sqlite:///taskflow.db en el archivo de configuración. La interacción con las tablas se realiza mediante el ORM Flask-SQLAlchemy, eliminando la necesidad de escribir código SQL nativo y reduciendo la vulnerabilidad a ataques de inyección SQL.
Mapeo de Relaciones Estructurales

Las entidades de dominio implementan relaciones complejas con restricciones de integridad:

    User → Project (1:N): Un usuario puede ser propietario (owner) de múltiples proyectos. Se define una clave foránea (owner_id) con una relación que aplica eliminación en cascada (cascade='all, delete-orphan').

    Project → Task (1:N): Contenedor estructural básico. Al eliminar un proyecto del sistema, todas las tareas asociadas son destruidas automáticamente para mantener la consistencia relacional.

    User → Task (1:N): Relación de asignación de responsabilidades operativas mediante Task.assigned_to.

Evolución del Esquema (Migrations)

A través de la extensión Flask-Migrate (basada en Alembic), el ciclo de vida del software soporta cambios incrementales en las estructuras de datos sin pérdida de información. Los comandos CLI flask db migrate automatizan la detección de discrepancias entre los modelos declarados en Python y el estado físico de las tablas, traduciendo los cambios en scripts secuenciales de migración (upgrade / downgrade).
### 5. Concurrencia y Multiprocesamiento (Background Services)

Una de las características críticas de TaskFlow es la ejecución de procesos de soporte de manera asíncrona para no bloquear el hilo de ejecución principal encargado de responder a las peticiones del usuario web.

Para esto, se diseñaron dos servicios basados en hilos daemon independientes (Programación Concurrente con threading), coordinados con el ciclo de vida de la aplicación Flask a través del contexto (app.app_context()).
Hilo 1: Servicio de Monitoreo de Tareas (NotificationService)

    Frecuencia: Se ejecuta de forma cíclica cada 60 segundos (time.sleep(60)).

    Operación: Realiza una consulta reactiva a la base de datos local buscando aquellas tareas 
    cuyo estado sea diferente a 'completed' y cuya fecha de vencimiento (due_date) sea inferior al
    tiempo actual de la máquina (datetime.utcnow()).

    Efecto: Genera de forma automatizada un registro en la tabla Notification asignado al usuario 
    responsable de la tarea y al dueño del proyecto, persistiendo la alerta de desfase cronológico.

Hilo 2: Servicio de Auditoría del Sistema (LogService)

    Frecuencia: Se ejecuta cada 30 segundos.

    Operación: Para optimizar las operaciones de Entrada/Salida (I/O), este hilo evalúa los registros
    históricos del modelo LogEntry utilizando un puntero de control incremental (self.last_log_id).

    Efecto: Extrae los nuevos logs generados en memoria y los añade por lotes (batch writing) de 
    forma persistente a un archivo plano plano en disco local (data/output/system_audit.csv) 
    utilizando la librería estándar csv de Python. Al configurarse como hilo daemon, no detiene 
    el apagado del servidor principal.

### 6. Uso del Servidor Local (Localhost Environment)

El despliegue de desarrollo se ejecuta localmente sobre la interfaz de bucle de retorno (loopback) localhost utilizando la dirección IP estandarizada 127.0.0.1 en conjunto con el puerto por defecto de Flask 5000.
Flujo Operacional de una Solicitud HTTP
Plaintext
 
      [Cliente: Navegador] 
              │ (Petición HTTP p.ej. POST /project/create)
              ▼
      [Localhost:5000 / Servidor Werkzeug WSGI de Flask]
              │
              ├── Enruta la petición hacia `project_routes.py`
              │
              ├── Capa Control: Valida sesión activa (`@requires_login`)
              │
              ├── Capa Datos: Invoca `ProjectRepository.create(...)`
              │        │
              │        └── [ORM SQLAlchemy] ──> Inserta en `taskflow.db` (SQLite)
              │
              ├── Hilo de Auditoría: Crea `LogEntry` en paralelo
              │
              └── Capa Vista: Inyecta datos en `dashboard.html` vía Jinja2
              ▼
      [Cliente: Renderizado HTML en Pantalla]

El servidor local embebido implementa el motor de servicio web compatible con la especificación 
WSGI (servidor Werkzeug), operando en modo síncrono para las peticiones de usuario pero tolerando
la bifurcación asíncrona de los hilos de servicios previamente detallados en la sección de concurrencia.

### 7. Conclusiones

La separación modular mediante patrones de diseño estructurales como MVC y Repository otorga 
al software alta mantenibilidad, permitiendo cambiar el motor de persistencia física 
(p.ej., de SQLite a PostgreSQL) modificando únicamente la capa de infraestructura sin 
alterar la lógica de negocio ni la interfaz de rutas.

El manejo de la concurrencia nativa de Python a través de hilos asíncronos daemon demuestra 
cómo resolver tareas intensivas de procesamiento y auditoría en tiempo real sin deteriorar la 
experiencia de usuario (user experience), manteniendo tiempos de respuesta inmediatos en el servidor localhost.