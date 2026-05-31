"""
Repository de Usuario.

Maneja CRUD de usuarios en la base de datos.
"""

from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


class UserRepository:
    """Repositorio para operaciones CRUD de User."""
    
    @staticmethod
    def create(username, email, password, name, role='member'):
        """
        Crea un nuevo usuario.
        
        Args:
            username (str): Nombre de usuario único
            email (str): Email único
            password (str): Contraseña (será hasheada)
            name (str): Nombre completo
            role (str): Rol ('admin' o 'member')
        
        Returns:
            User: Usuario creado
        """
        # Verificar si ya existe
        if User.query.filter_by(username=username).first():
            raise ValueError(f"Usuario {username} ya existe")
        
        if User.query.filter_by(email=email).first():
            raise ValueError(f"Email {email} ya registrado")
        
        # Crear usuario
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            name=name,
            role=role
        )
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def get_by_id(user_id):
        """
        Obtiene un usuario por ID.
        
        Args:
            user_id (int): ID del usuario
        
        Returns:
            User: Usuario encontrado o None
        """
        return User.query.get(user_id)
    
    @staticmethod
    def get_by_username(username):
        """
        Obtiene un usuario por nombre de usuario.
        
        Args:
            username (str): Nombre de usuario
        
        Returns:
            User: Usuario encontrado o None
        """
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email):
        """
        Obtiene un usuario por email.
        
        Args:
            email (str): Email del usuario
        
        Returns:
            User: Usuario encontrado o None
        """
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_all():
        """
        Obtiene todos los usuarios.
        
        Returns:
            list: Lista de usuarios
        """
        return User.query.all()
    
    @staticmethod
    def update(user_id, **kwargs):
        """
        Actualiza un usuario.
        
        Args:
            user_id (int): ID del usuario
            **kwargs: Campos a actualizar (name, email, role)
        
        Returns:
            User: Usuario actualizado
        """
        user = User.query.get(user_id)
        
        if not user:
            return None
        
        if 'name' in kwargs:
            user.name = kwargs['name']
        if 'email' in kwargs:
            user.email = kwargs['email']
        if 'role' in kwargs:
            user.role = kwargs['role']
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user_id):
        """
        Elimina un usuario.
        
        Args:
            user_id (int): ID del usuario
        
        Returns:
            bool: True si se eliminó, False si no existe
        """
        user = User.query.get(user_id)
        
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    @staticmethod
    def verify_password(username, password):
        """
        Verifica la contraseña de un usuario.
        
        Args:
            username (str): Nombre de usuario
            password (str): Contraseña a verificar
        
        Returns:
            User: Usuario si credenciales son válidas, None si no
        """
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            return user
        
        return None