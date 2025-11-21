"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Funciones helper para respuestas JSON estandarizadas
"""
from flask import jsonify

def respuesta_exitosa(datos=None, mensaje="Operación exitosa", codigo=200):
    """Genera respuesta exitosa estandarizada"""
    respuesta = {
        'exito': True,
        'mensaje': mensaje
    }
    if datos is not None:
        respuesta['datos'] = datos
    return jsonify(respuesta), codigo

def respuesta_error(mensaje="Error en la operación", error=None, codigo=400):
    """Genera respuesta de error estandarizada"""
    respuesta = {
        'exito': False,
        'mensaje': mensaje
    }
    if error:
        respuesta['error'] = error
    return jsonify(respuesta), codigo

def respuesta_no_autorizado(mensaje="No autorizado"):
    """Genera respuesta de no autorizado"""
    return respuesta_error(mensaje, 'no_autorizado', 401)

def respuesta_no_encontrado(mensaje="Recurso no encontrado"):
    """Genera respuesta de recurso no encontrado"""
    return respuesta_error(mensaje, 'no_encontrado', 404)
