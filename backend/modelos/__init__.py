"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Módulo de modelos de base de datos.
             Inicializa SQLAlchemy y exporta modelos.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .usuario import Usuario
from .analisis import Analisis

__all__ = ['db', 'Usuario', 'Analisis', 'inicializar_base_datos']


def inicializar_base_datos():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Crea todas las tablas en la base de datos e inicializa usuario admin
    Argumentos entrada: Ninguno
    Returns: None
    Modificaciones: Ninguna
    """
    from flask import current_app
    import os

    try:
        db.create_all()

        usuario_admin = Usuario.query.filter_by(
            nombre_usuario=current_app.config['USUARIO_ADMIN']
        ).first()

        if not usuario_admin:
            usuario_admin = Usuario(
                nombre_usuario=current_app.config['USUARIO_ADMIN'],
                contrasena=current_app.config['CONTRASENA_ADMIN']
            )
            db.session.add(usuario_admin)
            db.session.commit()

            print(f"✅ Usuario administrador creado: {current_app.config['USUARIO_ADMIN']}")
        else:
            print(f"ℹ️  Usuario administrador ya existe: {current_app.config['USUARIO_ADMIN']}")
    except Exception as e:
        print(f"⚠️  Error al inicializar base de datos: {e}")
