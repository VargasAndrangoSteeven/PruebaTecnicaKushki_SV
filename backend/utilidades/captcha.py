"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Sistema de captcha matemático local (sin servicios externos)
             Genera operaciones matemáticas simples para validar usuarios
Argumentos entrada: Ninguno
Returns: Funciones de generación y validación de captcha
Modificaciones: Ninguna
"""

import random
import secrets
from datetime import datetime, timedelta


captchas_activos = {}


def limpiar_captchas_expirados():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Elimina captchas expirados (más de 5 minutos)
    Argumentos entrada: Ninguno
    Returns: None
    Modificaciones: Ninguna
    """
    ahora = datetime.now()
    captchas_expirados = []
    
    for token, datos in captchas_activos.items():
        if ahora - datos['creado'] > timedelta(minutes=5):
            captchas_expirados.append(token)
    
    for token in captchas_expirados:
        del captchas_activos[token]


def generar_captcha():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Genera un captcha matemático simple
    Argumentos entrada: Ninguno
    Returns:
        dict: {
            'token': str (identificador único),
            'pregunta': str (operación matemática),
            'tipo': str (tipo de operación)
        }
    Modificaciones: Ninguna
    """
    limpiar_captchas_expirados()

    print(f"[CAPTCHA DEBUG] Generando nuevo captcha - Captchas activos antes: {len(captchas_activos)}")

    token = secrets.token_urlsafe(32)
    
    operaciones = ['suma', 'resta', 'multiplicacion']
    tipo_operacion = random.choice(operaciones)
    
    if tipo_operacion == 'suma':
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        respuesta = num1 + num2
        pregunta = f"¿Cuánto es {num1} + {num2}?"
    
    elif tipo_operacion == 'resta':
        num1 = random.randint(10, 30)
        num2 = random.randint(1, 10)
        respuesta = num1 - num2
        pregunta = f"¿Cuánto es {num1} - {num2}?"
    
    else:
        num1 = random.randint(2, 10)
        num2 = random.randint(2, 10)
        respuesta = num1 * num2
        pregunta = f"¿Cuánto es {num1} × {num2}?"
    
    captchas_activos[token] = {
        'respuesta': respuesta,
        'creado': datetime.now(),
        'intentos': 0
    }

    print(f"[CAPTCHA DEBUG] Captcha generado - Pregunta: '{pregunta}', Respuesta: {respuesta}, Token: {token[:20]}...")
    print(f"[CAPTCHA DEBUG] Captchas activos después: {len(captchas_activos)}")

    return {
        'token': token,
        'pregunta': pregunta,
        'tipo': tipo_operacion
    }


def validar_captcha(token, respuesta_usuario):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Valida la respuesta del captcha
    Argumentos entrada:
        token (str): Token del captcha
        respuesta_usuario (int): Respuesta proporcionada por el usuario
    Returns:
        tuple: (bool exito, str mensaje)
    Modificaciones: Ninguna
    """
    print(f"[CAPTCHA DEBUG] Validando captcha - Token: {token[:20]}..., Respuesta: {respuesta_usuario}")
    print(f"[CAPTCHA DEBUG] Captchas activos: {len(captchas_activos)} tokens")

    if token not in captchas_activos:
        print(f"[CAPTCHA DEBUG] Token NO encontrado en captchas activos")
        return False, "Captcha inválido o expirado"

    datos_captcha = captchas_activos[token]
    print(f"[CAPTCHA DEBUG] Token encontrado - Respuesta esperada: {datos_captcha['respuesta']}, Intentos: {datos_captcha['intentos']}")

    if datos_captcha['intentos'] >= 3:
        print(f"[CAPTCHA DEBUG] Demasiados intentos - eliminando token")
        del captchas_activos[token]
        return False, "Demasiados intentos incorrectos"

    datos_captcha['intentos'] += 1

    try:
        respuesta_int = int(respuesta_usuario)
        print(f"[CAPTCHA DEBUG] Respuesta convertida a int: {respuesta_int}")
    except (ValueError, TypeError):
        print(f"[CAPTCHA DEBUG] Error al convertir respuesta a int")
        return False, "Respuesta inválida"

    if respuesta_int == datos_captcha['respuesta']:
        print(f"[CAPTCHA DEBUG] ✓ Respuesta CORRECTA - eliminando token")
        del captchas_activos[token]
        return True, "Captcha validado correctamente"
    else:
        print(f"[CAPTCHA DEBUG] ✗ Respuesta INCORRECTA - Intentos restantes: {3 - datos_captcha['intentos']}")
        return False, f"Respuesta incorrecta. Intentos restantes: {3 - datos_captcha['intentos']}"


def obtener_nuevo_captcha_si_falla(token_anterior):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Si el captcha falló, genera uno nuevo
    Argumentos entrada:
        token_anterior (str): Token del captcha anterior
    Returns:
        dict: Nuevo captcha
    Modificaciones: Ninguna
    """
    if token_anterior in captchas_activos:
        del captchas_activos[token_anterior]
    
    return generar_captcha()
