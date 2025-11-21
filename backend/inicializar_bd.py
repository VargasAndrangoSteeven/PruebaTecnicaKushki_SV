"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Script para inicializar la base de datos con tablas y usuario admin
Argumentos entrada: Ninguno
Returns: None
Modificaciones: Ninguna
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from modelos import Usuario
from dotenv import load_dotenv

load_dotenv()


def inicializar_base_datos():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Crea las tablas de la base de datos y el usuario administrador
    """
    with app.app_context():
        print("=" * 60)
        print("🗄️  INICIALIZANDO BASE DE DATOS")
        print("=" * 60)
        
        print("\n📋 Creando tablas...")
        db.create_all()
        print("✅ Tablas creadas exitosamente")
        
        usuario_admin_nombre = app.config['USUARIO_ADMIN']
        usuario_admin = Usuario.buscar_por_nombre(usuario_admin_nombre)
        
        if usuario_admin:
            print(f"\nℹ️  El usuario administrador '{usuario_admin_nombre}' ya existe")
        else:
            print(f"\n👤 Creando usuario administrador: {usuario_admin_nombre}")
            
            usuario_admin = Usuario(
                nombre_usuario=usuario_admin_nombre,
                contrasena=app.config['CONTRASENA_ADMIN']
            )
            
            db.session.add(usuario_admin)
            db.session.commit()
            
            print(f"✅ Usuario administrador creado exitosamente")
            print(f"   Usuario: {usuario_admin_nombre}")
            print(f"   Contraseña: {app.config['CONTRASENA_ADMIN']}")
        
        total_usuarios = Usuario.query.count()
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"   Total de usuarios: {total_usuarios}")
        
        print("\n" + "=" * 60)
        print("✅ INICIALIZACIÓN COMPLETADA")
        print("=" * 60)


if __name__ == '__main__':
    try:
        inicializar_base_datos()
    except Exception as e:
        print(f"\n❌ ERROR al inicializar base de datos:")
        print(f"   {str(e)}")
        sys.exit(1)
