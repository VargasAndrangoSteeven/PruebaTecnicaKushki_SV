"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Modelo de base de datos para Usuario.
             Gestiona autenticación y datos de usuario.
Argumentos entrada: Ninguno
Returns: Clase Usuario (modelo SQLAlchemy)
Modificaciones: Ninguna
"""

from datetime import datetime
import bcrypt
from . import db


class Usuario(db.Model):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Modelo de Usuario para autenticación
    """
    
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False, index=True)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fecha_ultima_sesion = db.Column(db.DateTime)
    activo = db.Column(db.Boolean, default=True, nullable=False)

    analisis = db.relationship('Analisis', backref='usuario', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, nombre_usuario, contrasena):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Constructor del modelo Usuario
        Argumentos entrada:
            nombre_usuario (str): Nombre de usuario único
            contrasena (str): Contraseña en texto plano (se hasheará)
        Returns: Instancia de Usuario
        Modificaciones: Ninguna
        """
        self.nombre_usuario = nombre_usuario
        self.establecer_contrasena(contrasena)
    
    def establecer_contrasena(self, contrasena):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Hashea y almacena la contraseña de forma segura
        Argumentos entrada:
            contrasena (str): Contraseña en texto plano
        Returns: None
        Modificaciones: Ninguna
        """
        sal = bcrypt.gensalt(rounds=12)
        self.contrasena_hash = bcrypt.hashpw(
            contrasena.encode('utf-8'), 
            sal
        ).decode('utf-8')
    
    def verificar_contrasena(self, contrasena):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Verifica si la contraseña proporcionada es correcta
        Argumentos entrada:
            contrasena (str): Contraseña a verificar
        Returns:
            bool: True si la contraseña es correcta, False si no
        Modificaciones: Ninguna
        """
        return bcrypt.checkpw(
            contrasena.encode('utf-8'),
            self.contrasena_hash.encode('utf-8')
        )
    
    def actualizar_ultima_sesion(self):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Actualiza la fecha de última sesión del usuario
        Argumentos entrada: Ninguno
        Returns: None
        Modificaciones: Ninguna
        """
        self.fecha_ultima_sesion = datetime.utcnow()
        db.session.commit()
    
    def obtener_analisis_recientes(self, limite=10):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Obtiene los análisis más recientes del usuario
        Argumentos entrada:
            limite (int): Número máximo de análisis a retornar
        Returns:
            list: Lista de análisis ordenados por fecha (más recientes primero)
        Modificaciones: Ninguna
        """
        return self.analisis.order_by(
            db.desc('fecha_analisis')
        ).limit(limite).all()
    
    def contar_analisis(self):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Cuenta el total de análisis del usuario
        Argumentos entrada: Ninguno
        Returns:
            int: Número total de análisis
        Modificaciones: Ninguna
        """
        return self.analisis.count()
    
    def a_dict(self, incluir_analisis=False):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Convierte el usuario a diccionario (para JSON)
        Argumentos entrada:
            incluir_analisis (bool): Si True, incluye lista de análisis
        Returns:
            dict: Representación del usuario en diccionario
        Modificaciones: Ninguna
        """
        datos = {
            'id': self.id,
            'nombre_usuario': self.nombre_usuario,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_ultima_sesion': self.fecha_ultima_sesion.isoformat() if self.fecha_ultima_sesion else None,
            'activo': self.activo,
            'total_analisis': self.contar_analisis()
        }
        
        if incluir_analisis:
            datos['analisis_recientes'] = [
                analisis.a_dict() for analisis in self.obtener_analisis_recientes(5)
            ]
        
        return datos
    
    def __repr__(self):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Representación en string del usuario
        """
        return f'<Usuario {self.nombre_usuario}>'
    
    @staticmethod
    def buscar_por_nombre(nombre_usuario):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Busca un usuario por su nombre de usuario
        Argumentos entrada:
            nombre_usuario (str): Nombre de usuario a buscar
        Returns:
            Usuario o None: Usuario encontrado o None
        Modificaciones: Ninguna
        """
        return Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
    
    @staticmethod
    def existe_usuario(nombre_usuario):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Verifica si existe un usuario con ese nombre
        Argumentos entrada:
            nombre_usuario (str): Nombre de usuario a verificar
        Returns:
            bool: True si existe, False si no
        Modificaciones: Ninguna
        """
        return Usuario.query.filter_by(nombre_usuario=nombre_usuario).first() is not None
