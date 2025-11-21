"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Funciones de validación para inputs de usuario
"""
import re
import os
from werkzeug.utils import secure_filename

def validar_contrasena(contrasena):
    """Valida que la contraseña cumpla requisitos de seguridad"""
    if len(contrasena) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not re.search(r'[A-Z]', contrasena):
        return False, "La contraseña debe contener al menos una mayúscula"
    
    if not re.search(r'[0-9]', contrasena):
        return False, "La contraseña debe contener al menos un número"
    
    if not re.search(r'[.,\-_]', contrasena):
        return False, "La contraseña debe contener al menos un símbolo (. , - _)"
    
    return True, "Contraseña válida"

def validar_nombre_usuario(nombre):
    """Valida el nombre de usuario"""
    if len(nombre) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres"
    
    if len(nombre) > 50:
        return False, "El nombre de usuario no puede exceder 50 caracteres"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', nombre):
        return False, "El nombre de usuario solo puede contener letras, números y guiones bajos"
    
    return True, "Nombre de usuario válido"

def validar_tipo_archivo(archivo):
    """Valida que el archivo sea una imagen"""
    extensiones_permitidas = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    return '.' in archivo.filename and            archivo.filename.rsplit('.', 1)[1].lower() in extensiones_permitidas

def validar_tamano_archivo(archivo, tamano_maximo=5*1024*1024):
    """Valida el tamaño del archivo"""
    archivo.seek(0, os.SEEK_END)
    tamano = archivo.tell()
    archivo.seek(0)
    return tamano <= tamano_maximo

def es_imagen_valida(archivo):
    """Verifica que el archivo es una imagen válida"""
    if not archivo:
        return False, "No se proporcionó ningún archivo"
    
    if not validar_tipo_archivo(archivo):
        return False, "Tipo de archivo no permitido. Solo se permiten: jpg, jpeg, png, gif, webp"
    
    if not validar_tamano_archivo(archivo):
        return False, "El archivo es demasiado grande. Máximo 5MB"
    
    return True, "Imagen válida"
