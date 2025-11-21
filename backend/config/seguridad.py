"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Configuración de seguridad de la aplicación.
             Incluye headers de seguridad, CORS, rate limiting.
Argumentos entrada: Ninguno
Returns: Funciones de configuración de seguridad
Modificaciones: Ninguna
"""

import secrets
from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta


def configurar_headers_seguridad(app):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Configura headers de seguridad HTTP para proteger la aplicación
    Argumentos entrada:
        app: Instancia de Flask
    Returns: None
    Modificaciones: Ninguna
    """
    
    @app.after_request
    def agregar_headers_seguridad(response):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Agrega headers de seguridad a cada respuesta
        """
        
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https://api.imagga.com https://vision.googleapis.com;"
        )
        
        response.headers['X-Frame-Options'] = 'DENY'
        
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        if request.is_secure:
            response.headers['Strict-Transport-Security'] = (
                'max-age=31536000; includeSubDomains'
            )
        
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        response.headers['Permissions-Policy'] = (
            'geolocation=(), microphone=(), camera=()'
        )
        
        return response


def generar_clave_segura(longitud=32):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Genera una clave segura aleatoria
    Argumentos entrada:
        longitud (int): Longitud de la clave en bytes
    Returns:
        str: Clave segura en hexadecimal
    Modificaciones: Ninguna
    """
    return secrets.token_hex(longitud)


intentos_peticiones = {}


def limitar_peticiones(limite_por_minuto=10):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Decorador para limitar número de peticiones por usuario
    Argumentos entrada:
        limite_por_minuto (int): Número máximo de peticiones por minuto
    Returns:
        Función decoradora
    Modificaciones: Ninguna
    """
    
    def decorador(funcion):
        @wraps(funcion)
        def funcion_decorada(*args, **kwargs):
            identificador_cliente = request.remote_addr
            
            ahora = datetime.now()
            
            intentos_peticiones_limpio = {}
            for cliente, intentos in intentos_peticiones.items():
                intentos_recientes = [
                    tiempo for tiempo in intentos 
                    if ahora - tiempo < timedelta(minutes=1)
                ]
                if intentos_recientes:
                    intentos_peticiones_limpio[cliente] = intentos_recientes
            
            intentos_peticiones.clear()
            intentos_peticiones.update(intentos_peticiones_limpio)
            
            if identificador_cliente not in intentos_peticiones:
                intentos_peticiones[identificador_cliente] = []
            
            intentos_cliente = intentos_peticiones[identificador_cliente]
            
            if len(intentos_cliente) >= limite_por_minuto:
                return jsonify({
                    'exito': False,
                    'mensaje': 'Demasiadas peticiones. Intenta nuevamente en un minuto.',
                    'error': 'limite_excedido'
                }), 429
            
            intentos_peticiones[identificador_cliente].append(ahora)
            
            return funcion(*args, **kwargs)
        
        return funcion_decorada
    return decorador


def validar_origen_peticion(app):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Valida que las peticiones vengan del frontend autorizado
    Argumentos entrada:
        app: Instancia de Flask
    Returns: None
    Modificaciones: Ninguna
    """
    
    @app.before_request
    def verificar_origen():
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Verifica el origen de cada petición
        """
        
        if request.path == '/api/salud':
            return None
        
        if app.config['FLASK_ENV'] == 'desarrollo':
            return None
        
        origen = request.headers.get('Origin')
        if origen and origen != app.config['URL_FRONTEND']:
            return jsonify({
                'exito': False,
                'mensaje': 'Origen no autorizado',
                'error': 'origen_no_autorizado'
            }), 403
        
        return None
