"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Rutas de autenticación (registro, login, logout)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from servicios.servicio_auth import ServicioAuth
from utilidades.respuestas import respuesta_exitosa, respuesta_error
from utilidades.decoradores import requiere_json
from config.seguridad import limitar_peticiones
from utilidades.captcha import generar_captcha, validar_captcha

autenticacion_bp = Blueprint('autenticacion', __name__)


@autenticacion_bp.route('/captcha', methods=['GET'])
def obtener_captcha():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para obtener un nuevo captcha matemático
    """
    try:
        captcha = generar_captcha()
        return respuesta_exitosa(
            datos=captcha,
            mensaje="Captcha generado"
        )
    except Exception as e:
        return respuesta_error(f"Error al generar captcha: {str(e)}", codigo=500)


@autenticacion_bp.route('/registrar', methods=['POST'])
@requiere_json
@limitar_peticiones(limite_por_minuto=5)
def registrar():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para registrar nuevo usuario con validación de captcha
    """
    try:
        datos = request.get_json()
        
        if not datos.get('nombre_usuario') or not datos.get('contrasena'):
            return respuesta_error("nombre_usuario y contrasena son requeridos")
        
        token_captcha = datos.get('captcha_token')
        respuesta_captcha = datos.get('captcha_respuesta')
        
        if not token_captcha or not respuesta_captcha:
            return respuesta_error("Se requiere completar el captcha")
        
        captcha_valido, mensaje_captcha = validar_captcha(token_captcha, respuesta_captcha)

        if not captcha_valido:
            return respuesta_error(mensaje_captcha)
        
        nombre_usuario = datos['nombre_usuario']
        contrasena = datos['contrasena']
        
        exito, mensaje, usuario = ServicioAuth.registrar_usuario(nombre_usuario, contrasena)
        
        if not exito:
            return respuesta_error(mensaje)
        
        return respuesta_exitosa(
            datos=usuario.a_dict(),
            mensaje=mensaje,
            codigo=201
        )
        
    except Exception as e:
        return respuesta_error(f"Error al registrar usuario: {str(e)}", codigo=500)


@autenticacion_bp.route('/iniciar-sesion', methods=['POST'])
@requiere_json
@limitar_peticiones(limite_por_minuto=10)
def iniciar_sesion():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para iniciar sesión
    """
    try:
        datos = request.get_json()
        
        if not datos.get('nombre_usuario') or not datos.get('contrasena'):
            return respuesta_error("nombre_usuario y contrasena son requeridos")
        
        nombre_usuario = datos['nombre_usuario']
        contrasena = datos['contrasena']
        
        exito, mensaje, token, usuario = ServicioAuth.iniciar_sesion(nombre_usuario, contrasena)
        
        if not exito:
            return respuesta_error(mensaje, codigo=401)
        
        return respuesta_exitosa(
            datos={
                'token': token,
                'usuario': usuario.a_dict()
            },
            mensaje=mensaje
        )
        
    except Exception as e:
        return respuesta_error(f"Error al iniciar sesión: {str(e)}", codigo=500)


@autenticacion_bp.route('/verificar', methods=['GET'])
@jwt_required()
def verificar_token():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para verificar token JWT
    """
    try:
        usuario_id = get_jwt_identity()
        exito, usuario = ServicioAuth.verificar_token(usuario_id)
        
        if not exito:
            return respuesta_error("Token inválido", codigo=401)
        
        return respuesta_exitosa(
            datos=usuario.a_dict(),
            mensaje="Token válido"
        )
        
    except Exception as e:
        return respuesta_error(f"Error al verificar token: {str(e)}", codigo=500)


@autenticacion_bp.route('/cerrar-sesion', methods=['POST'])
@jwt_required()
def cerrar_sesion():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para cerrar sesión
    """
    return respuesta_exitosa(mensaje="Sesión cerrada exitosamente")
