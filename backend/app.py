"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Punto de entrada principal de la aplicación Flask.
             Inicializa la app, configura middleware, registra rutas.
Argumentos entrada: Ninguno
Returns: Aplicación Flask configurada
Modificaciones: Ninguna
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from config.configuracion import Configuracion
from config.seguridad import configurar_headers_seguridad

from modelos import db, inicializar_base_datos

from rutas.autenticacion import autenticacion_bp
from rutas.analisis import analisis_bp

load_dotenv()


def crear_aplicacion(configuracion_clase=Configuracion):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Factory function para crear y configurar la aplicación Flask
    Argumentos entrada:
        configuracion_clase: Clase de configuración a usar (por defecto Configuracion)
    Returns:
        app: Aplicación Flask configurada
    Modificaciones: Ninguna
    """

    app = Flask(__name__)

    app.config.from_object(configuracion_clase)

    directorio_base = os.path.abspath(os.path.dirname(__file__))
    os.makedirs(os.path.join(directorio_base, "datos"), exist_ok=True)
    os.makedirs(os.path.join(directorio_base, "cargas"), exist_ok=True)
    os.makedirs(os.path.join(directorio_base, "logs"), exist_ok=True)
    os.makedirs(os.path.join(directorio_base, "credenciales"), exist_ok=True)

    inicializar_extensiones(app)

    registrar_blueprints(app)

    registrar_manejadores_errores(app)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"⚠️  Error al crear tablas: {e}")

    return app


def inicializar_extensiones(app):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Inicializa las extensiones de Flask (CORS, JWT, BD)
    Argumentos entrada:
        app: Instancia de Flask
    Returns: None
    Modificaciones: Ninguna
    """
    
    db.init_app(app)
    
    CORS(app, 
         origins=[app.config['URL_FRONTEND']],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    jwt = JWTManager(app)
    
    configurar_headers_seguridad(app)
    
    @jwt.expired_token_loader
    def token_expirado_callback(jwt_header, jwt_payload):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Callback cuando el token JWT ha expirado
        """
        return jsonify({
            'exito': False,
            'mensaje': 'El token ha expirado. Por favor, inicia sesión nuevamente.',
            'error': 'token_expirado'
        }), 401
    
    @jwt.invalid_token_loader
    def token_invalido_callback(error):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Callback cuando el token JWT es inválido
        """
        return jsonify({
            'exito': False,
            'mensaje': 'Token inválido. Por favor, inicia sesión nuevamente.',
            'error': 'token_invalido'
        }), 401
    
    @jwt.unauthorized_loader
    def token_faltante_callback(error):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Callback cuando no se proporciona token JWT
        """
        return jsonify({
            'exito': False,
            'mensaje': 'Se requiere autenticación. Token no proporcionado.',
            'error': 'token_faltante'
        }), 401


def registrar_blueprints(app):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Registra todos los blueprints (rutas) de la aplicación
    Argumentos entrada:
        app: Instancia de Flask
    Returns: None
    Modificaciones: Ninguna
    """
    
    app.register_blueprint(autenticacion_bp, url_prefix='/api/auth')
    
    app.register_blueprint(analisis_bp, url_prefix='/api')
    
    @app.route('/api/salud', methods=['GET'])
    def verificar_salud():
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Endpoint para verificar que la API está funcionando
        """
        return jsonify({
            'exito': True,
            'mensaje': 'API funcionando correctamente',
            'version': '1.0.0'
        }), 200
    
    @app.route('/', methods=['GET'])
    def inicio():
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Endpoint raíz de bienvenida
        """
        return jsonify({
            'mensaje': 'Bienvenido al Analizador Inteligente de Imágenes - API',
            'version': '1.0.0',
            'autor': 'Steeven Vargas',
            'endpoints': {
                'salud': '/api/salud',
                'autenticacion': {
                    'registrar': '/api/auth/registrar',
                    'iniciar_sesion': '/api/auth/iniciar-sesion',
                    'cerrar_sesion': '/api/auth/cerrar-sesion',
                    'verificar': '/api/auth/verificar'
                },
                'analisis': {
                    'analizar': '/api/analizar',
                    'historial': '/api/historial',
                    'detalle': '/api/historial/<id>',
                    'eliminar': '/api/historial/<id>'
                }
            }
        }), 200


def registrar_manejadores_errores(app):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Registra manejadores personalizados para errores HTTP
    Argumentos entrada:
        app: Instancia de Flask
    Returns: None
    Modificaciones: Ninguna
    """
    
    @app.errorhandler(404)
    def no_encontrado(error):
        """Error 404 - Recurso no encontrado"""
        return jsonify({
            'exito': False,
            'mensaje': 'Recurso no encontrado',
            'error': 'no_encontrado'
        }), 404
    
    @app.errorhandler(500)
    def error_servidor(error):
        """Error 500 - Error interno del servidor"""
        return jsonify({
            'exito': False,
            'mensaje': 'Error interno del servidor',
            'error': 'error_servidor'
        }), 500
    
    @app.errorhandler(400)
    def solicitud_incorrecta(error):
        """Error 400 - Solicitud incorrecta"""
        return jsonify({
            'exito': False,
            'mensaje': 'Solicitud incorrecta',
            'error': 'solicitud_incorrecta'
        }), 400
    
    @app.errorhandler(413)
    def archivo_muy_grande(error):
        """Error 413 - Archivo demasiado grande"""
        return jsonify({
            'exito': False,
            'mensaje': 'El archivo es demasiado grande. Máximo 5MB',
            'error': 'archivo_muy_grande'
        }), 413


app = crear_aplicacion()


if __name__ == '__main__':
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Ejecuta la aplicación Flask en modo desarrollo
    """
    
    puerto = int(os.getenv('PUERTO_BACKEND', 5077))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    app.run(
        host='0.0.0.0',
        port=puerto,
        debug=debug,
        ssl_context='adhoc' if os.getenv('USAR_SSL_DESARROLLO') == 'True' else None
    )
