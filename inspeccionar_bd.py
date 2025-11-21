"""
Script para inspeccionar la base de datos SQLite
Autor: Steeven Vargas
Fecha: Noviembre 2024
"""

import sqlite3
import os
from datetime import datetime

ruta_bd = os.path.join(os.path.dirname(__file__), 'backend', 'datos', 'app.db')

if not os.path.exists(ruta_bd):
    print(f"❌ Base de datos no encontrada en: {ruta_bd}")
    print("   Asegúrate de que el backend haya creado la base de datos.")
    exit(1)

conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

print("=" * 80)
print("INSPECCIÓN DE BASE DE DATOS - ANALIZADOR DE IMÁGENES")
print("=" * 80)
print()

print("📊 TABLAS EN LA BASE DE DATOS")
print("-" * 80)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
for tabla in tablas:
    print(f"  ✓ {tabla[0]}")
print()

print("👥 TABLA: USUARIOS")
print("-" * 80)
cursor.execute("SELECT COUNT(*) FROM usuarios")
total_usuarios = cursor.fetchone()[0]
print(f"Total de usuarios: {total_usuarios}")
print()

if total_usuarios > 0:
    cursor.execute("""
        SELECT id, nombre_usuario, fecha_creacion, fecha_ultima_sesion, activo
        FROM usuarios
        ORDER BY id
    """)

    usuarios = cursor.fetchall()
    print(f"{'ID':<5} {'Usuario':<20} {'Fecha Creación':<20} {'Última Sesión':<20} {'Activo':<10}")
    print("-" * 80)

    for u in usuarios:
        id_usuario, nombre, fecha_creacion, fecha_ultima, activo = u
        fecha_creacion_fmt = fecha_creacion[:19] if fecha_creacion else 'N/A'
        fecha_ultima_fmt = fecha_ultima[:19] if fecha_ultima else 'Nunca'
        activo_fmt = '✓ Sí' if activo else '✗ No'

        print(f"{id_usuario:<5} {nombre:<20} {fecha_creacion_fmt:<20} {fecha_ultima_fmt:<20} {activo_fmt:<10}")

    print()

    cursor.execute("""
        SELECT nombre_usuario, LENGTH(contrasena_hash), SUBSTR(contrasena_hash, 1, 30)
        FROM usuarios
    """)
    print("🔒 INFORMACIÓN DE CONTRASEÑAS (HASHES)")
    print("-" * 80)
    print(f"{'Usuario':<20} {'Long. Hash':<12} {'Hash (primeros 30 caracteres)'}")
    print("-" * 80)

    for u in cursor.fetchall():
        print(f"{u[0]:<20} {u[1]:<12} {u[2]}...")

    print()

print("🖼️  TABLA: ANÁLISIS")
print("-" * 80)
cursor.execute("SELECT COUNT(*) FROM analisis")
total_analisis = cursor.fetchone()[0]
print(f"Total de análisis: {total_analisis}")
print()

if total_analisis > 0:
    cursor.execute("""
        SELECT a.id, a.usuario_id, u.nombre_usuario, a.nombre_archivo,
               a.proveedor_ia, a.fecha_analisis
        FROM analisis a
        LEFT JOIN usuarios u ON a.usuario_id = u.id
        ORDER BY a.fecha_analisis DESC
        LIMIT 20
    """)

    analisis = cursor.fetchall()
    print(f"{'ID (UUID)':<38} {'User':<15} {'Archivo':<25} {'IA':<10} {'Fecha'}")
    print("-" * 120)

    for a in analisis:
        id_analisis, user_id, user_nombre, archivo, proveedor, fecha = a
        fecha_fmt = fecha[:19] if fecha else 'N/A'
        archivo_corto = archivo[:22] + '...' if len(archivo) > 25 else archivo

        print(f"{id_analisis[:36]:<38} {user_nombre or 'N/A':<15} {archivo_corto:<25} {proveedor:<10} {fecha_fmt}")

    print()

    cursor.execute("""
        SELECT u.nombre_usuario, COUNT(a.id) as total
        FROM usuarios u
        LEFT JOIN analisis a ON u.id = a.usuario_id
        GROUP BY u.id, u.nombre_usuario
        ORDER BY total DESC
    """)

    print("📈 ANÁLISIS POR USUARIO")
    print("-" * 80)
    print(f"{'Usuario':<30} {'Total Análisis'}")
    print("-" * 80)

    for fila in cursor.fetchall():
        print(f"{fila[0]:<30} {fila[1]}")

    print()

    cursor.execute("""
        SELECT proveedor_ia, COUNT(*) as total
        FROM analisis
        GROUP BY proveedor_ia
        ORDER BY total DESC
    """)

    print("🤖 ANÁLISIS POR PROVEEDOR DE IA")
    print("-" * 80)
    print(f"{'Proveedor':<20} {'Total Análisis'}")
    print("-" * 80)

    for fila in cursor.fetchall():
        print(f"{fila[0]:<20} {fila[1]}")

    print()

cursor.execute("PRAGMA database_list;")
print("💾 INFORMACIÓN DE LA BASE DE DATOS")
print("-" * 80)
for db_info in cursor.fetchall():
    print(f"Nombre: {db_info[1]}")
    print(f"Archivo: {db_info[2]}")

tamaño_bd = os.path.getsize(ruta_bd)
print(f"Tamaño: {tamaño_bd:,} bytes ({tamaño_bd / 1024:.2f} KB)")
print()

print("=" * 80)
print("✓ Inspección completada")
print("=" * 80)

conn.close()
