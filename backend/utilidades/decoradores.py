"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Decoradores personalizados para rutas
"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from modelos import Usuario

def requiere_autenticacion(funcion):
    """Decorador que requiere autenticación JWT"""
    @wraps(funcion)
    def funcion_decorada(*args, **kwargs):
        try:
            verify_jwt_in_request()
            usuario_id = get_jwt_identity()
            # Convertir a int (viene como string desde JWT)
            usuario = Usuario.query.get(int(usuario_id))

            if not usuario or not usuario.activo:
                return jsonify({
                    'exito': False,
                    'mensaje': 'Usuario no encontrado o inactivo',
                    'error': 'usuario_no_autorizado'
                }), 401

            return funcion(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'exito': False,
                'mensaje': 'Error de autenticación',
                'error': str(e)
            }), 401

    return funcion_decorada

def requiere_json(funcion):
    """Decorador que requiere Content-Type: application/json"""
    @wraps(funcion)
    def funcion_decorada(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                'exito': False,
                'mensaje': 'Content-Type debe ser application/json',
                'error': 'tipo_contenido_invalido'
            }), 400
        return funcion(*args, **kwargs)
    
    return funcion_decorada
