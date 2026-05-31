"""Repository de Proyecto."""

from app import db
from app.models.project import Project


class ProjectRepository:
    """Repositorio para operaciones CRUD de Project."""
    
    @staticmethod
    def create(name, description, owner_id):
        """
        Crea un nuevo proyecto.
        
        Args:
            name (str): Nombre del proyecto
            description (str): Descripción
            owner_id (int): ID del propietario
        
        Returns:
            Project: Proyecto creado
        """
        project = Project(
            name=name,
            description=description,
            owner_id=owner_id
        )
        
        db.session.add(project)
        db.session.commit()
        
        return project
    
    @staticmethod
    def get_by_id(project_id):
        """Obtiene un proyecto por ID."""
        return Project.query.get(project_id)
    
    @staticmethod
    def get_by_owner(owner_id):
        """
        Obtiene todos los proyectos de un usuario.
        
        Args:
            owner_id (int): ID del propietario
        
        Returns:
            list: Lista de proyectos
        """
        return Project.query.filter_by(owner_id=owner_id).all()
    
    @staticmethod
    def get_all():
        """Obtiene todos los proyectos."""
        return Project.query.all()
    
    @staticmethod
    def update(project_id, **kwargs):
        """
        Actualiza un proyecto.
        
        Args:
            project_id (int): ID del proyecto
            **kwargs: Campos a actualizar
        
        Returns:
            Project: Proyecto actualizado o None
        """
        project = Project.query.get(project_id)
        
        if not project:
            return None
        
        if 'name' in kwargs:
            project.name = kwargs['name']
        if 'description' in kwargs:
            project.description = kwargs['description']
        
        db.session.commit()
        return project
    
    @staticmethod
    def delete(project_id):
        """Elimina un proyecto."""
        project = Project.query.get(project_id)
        
        if not project:
            return False
        
        db.session.delete(project)
        db.session.commit()
        return True