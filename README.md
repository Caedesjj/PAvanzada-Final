

## API POSTMAN

Crea una colección "TaskFlow API"

Prueba estos endpoints:
GET - Listar todos los proyectos
GET http://127.0.0.1:5000/api/projects
POST - Crear proyecto
POST http://127.0.0.1:5000/api/projects

Content-Type: application/json

{
  "name": "Proyecto Test",
  "description": "Mi primer proyecto",
  "owner_id": 1
}


GET - Obtener proyecto con tareas
GET http://127.0.0.1:5000/api/projects/1
POST - Crear tarea
POST http://127.0.0.1:5000/api/projects/1/tasks
Content-Type: application/json

{
  "title": "Tarea Test",
  "description": "Mi primera tarea",
  "priority": "high",
  "due_date": "2026-06-01T18:00:00"
}


PUT - Actualizar tarea
PUT http://127.0.0.1:5000/api/tasks/1
Content-Type: application/json

{
  "status": "completed",
  "priority": "medium"
}
DELETE - Eliminar tarea
DELETE http://127.0.0.1:5000/api/tasks/1