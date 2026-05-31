"""
Rutas de Autenticación (Authentication Routes).

Maneja:
- Registro de usuarios
- Login
- Logout
"""

from flask import render_template, request, redirect, url_for, session, flash
from app import db
from app.repositories.user_repository import UserRepository
from app.models.log_entry import LogEntry


def register_auth_routes(app):
    """Registra las rutas de autenticación."""
    
    @app.route('/')
    def index():
        """
        Página de inicio.
        
        Redirige al dashboard si está autenticado, al login si no.
        """
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """
        Registro de nuevo usuario.
        
        GET: Muestra formulario de registro
        POST: Procesa registro y crea usuario
        """
        if request.method == 'POST':
            try:
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                name = request.form['name']
                
                # Crear usuario usando repository
                user = UserRepository.create(
                    username=username,
                    email=email,
                    password=password,
                    name=name,
                    role='member'
                )
                
                # Registrar en log
                log = LogEntry(
                    action=LogEntry.ACTION_USER_CREATED,
                    description=f"Usuario {username} registrado",
                    user_id=user.id
                )
                db.session.add(log)
                db.session.commit()
                
                flash('Registro exitoso. Inicia sesión', 'success')
                return redirect(url_for('login'))
            
            except ValueError as e:
                flash(str(e), 'error')
        
        return render_template('register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """
        Iniciar sesión.
        
        GET: Muestra formulario de login
        POST: Verifica credenciales y crea sesión
        """
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            # Verificar credenciales usando repository
            user = UserRepository.verify_password(username, password)
            
            if user:
                # Crear sesión
                session['user_id'] = user.id
                session['username'] = user.username
                session['user_role'] = user.role
                
                # Registrar en log
                log = LogEntry(
                    action=LogEntry.ACTION_USER_LOGIN,
                    description=f"Usuario {username} inició sesión",
                    user_id=user.id
                )
                db.session.add(log)
                db.session.commit()
                
                flash(f'¡Bienvenido {user.name}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Credenciales inválidas', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        """
        Cerrar sesión.
        
        Limpia la sesión y registra el logout en logs.
        """
        user_id = session.get('user_id')
        username = session.get('username')
        
        session.clear()
        
        # Registrar en log
        if user_id:
            log = LogEntry(
                action=LogEntry.ACTION_USER_LOGOUT,
                description=f"Usuario {username} cerró sesión",
                user_id=user_id
            )
            db.session.add(log)
            db.session.commit()
        
        flash('Has cerrado sesión', 'success')
        return redirect(url_for('login'))