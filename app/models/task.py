from app import db


# modelo de tarea con campos de id, título y estado
class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    status = db.Column(db.String(20), default="pending")
