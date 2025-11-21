"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Servicio de autenticación y gestión de usuarios
"""

from modelos import db, Usuario
from flask_jwt_extended import create_access_token
from utilidades.validadores import validar_contrasena, validar_nombre_usuario


class ServicioAuth:
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Gestión de autenticación de usuarios
    """
    
    @staticmethod
    def registrar_usuario(nombre_usuario, contrasena):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Registra un nuevo usuario
        Argumentos entrada:
            nombre_usuario (str): Nombre de usuario
            contrasena (str): Contraseña
        Returns:
            tuple: (exito, mensaje, usuario)
        Modificaciones: Ninguna
        """
        valido, mensaje = validar_nombre_usuario(nombre_usuario)
        if not valido:
            return False, mensaje, None
        
        valido, mensaje = validar_contrasena(contrasena)
        if not valido:
            return False, mensaje, None
        
        if Usuario.existe_usuario(nombre_usuario):
            return False, "El nombre de usuario ya está en uso", None
        
        try:
            nuevo_usuario = Usuario(
                nombre_usuario=nombre_usuario,
                contrasena=contrasena
            )
            
            db.session.add(nuevo_usuario)
            db.session.commit()
            
            return True, "Usuario registrado exitosamente", nuevo_usuario
            
        except Exception as e:
            db.session.rollback()
            return False, f"Error al registrar usuario: {str(e)}", None
    
    @staticmethod
    def iniciar_sesion(nombre_usuario, contrasena):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Inicia sesión y genera token JWT
        Argumentos entrada:
            nombre_usuario (str): Nombre de usuario
            contrasena (str): Contraseña
        Returns:
            tuple: (exito, mensaje, token, usuario)
        Modificaciones: Ninguna
        """
        usuario = Usuario.buscar_por_nombre(nombre_usuario)
        
        if not usuario:
            return False, "Usuario o contraseña incorrectos", None, None
        
        if not usuario.verificar_contrasena(contrasena):
            return False, "Usuario o contraseña incorrectos", None, None
        
        if not usuario.activo:
            return False, "Usuario inactivo", None, None
        
        usuario.actualizar_ultima_sesion()

        token = create_access_token(identity=str(usuario.id))

        return True, "Inicio de sesión exitoso", token, usuario
    
    @staticmethod
    def verificar_token(usuario_id):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Verifica que el token sea válido y el usuario exista
        Argumentos entrada:
            usuario_id (str): ID del usuario (como string desde JWT)
        Returns:
            tuple: (exito, usuario)
        Modificaciones: Ninguna
        """
        try:
            id_int = int(usuario_id)
        except (ValueError, TypeError):
            return False, None

        usuario = Usuario.query.get(id_int)

        if not usuario or not usuario.activo:
            return False, None

        return True, usuario
