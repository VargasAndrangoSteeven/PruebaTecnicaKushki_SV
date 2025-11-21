"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Archivo de configuración principal de Flask.
             Gestiona variables de entorno y configuración de la aplicación.
Argumentos entrada: Ninguno
Returns: Clase Configuracion con todas las variables
Modificaciones: Ninguna
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

DIRECTORIO_BASE = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Configuracion:
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Clase de configuración principal de Flask
    """
    

    SECRET_KEY = os.getenv('CLAVE_SECRETA', 'clave-desarrollo-no-usar-en-produccion')
    FLASK_ENV = os.getenv('FLASK_ENV', 'desarrollo')
    DEBUG = FLASK_ENV == 'desarrollo'
    TESTING = False
    

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'URL_BASE_DATOS',
        f'sqlite:///{os.path.join(DIRECTORIO_BASE, "datos", "app.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    

    JWT_SECRET_KEY = os.getenv('CLAVE_SECRETA_JWT', 'jwt-clave-desarrollo-no-usar-en-produccion')
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    tiempo_expiracion = int(os.getenv('TIEMPO_EXPIRACION_JWT', 24))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=tiempo_expiracion)
    

    MAX_CONTENT_LENGTH = int(os.getenv('TAMANO_MAXIMO_ARCHIVO', 5 * 1024 * 1024))  # 5MB
    
    DIRECTORIO_CARGAS = os.path.join(DIRECTORIO_BASE, 'cargas')
    os.makedirs(DIRECTORIO_CARGAS, exist_ok=True)
    
    EXTENSIONES_PERMITIDAS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
    TIPOS_MIME_PERMITIDOS = [
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/gif',
        'image/webp'
    ]
    
    
    
    CREDENCIALES_GOOGLE = os.path.join(
        DIRECTORIO_BASE,
        os.getenv('CREDENCIALES_GOOGLE', './credenciales/google-vision.json')
    )
    
    IMAGGA_API_KEY = os.getenv('IMAGGA_API_KEY', '')
    IMAGGA_API_SECRET = os.getenv('IMAGGA_API_SECRET', '')
    IMAGGA_ENDPOINT = os.getenv('IMAGGA_ENDPOINT', 'https://api.imagga.com/v2/tags')
    
    
    
    FRASE_SEGURIDAD_GPG = os.getenv('FRASE_SEGURIDAD_GPG', 'frase-desarrollo')
    
    
    
    URL_FRONTEND = os.getenv('URL_FRONTEND', 'https://localhost:3000')
    
    
    
    LIMITE_PETICIONES_POR_MINUTO = int(os.getenv('LIMITE_PETICIONES_POR_MINUTO', 10))
    
    
    
    NIVEL_LOG = os.getenv('NIVEL_LOG', 'DEBUG')
    DIRECTORIO_LOGS = os.path.join(DIRECTORIO_BASE, 'logs')
    os.makedirs(DIRECTORIO_LOGS, exist_ok=True)
    
    
    
    RECAPTCHA_SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY', '')
    RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY', '')
    
    
    
    USUARIO_ADMIN = os.getenv('USUARIO_ADMIN', 'admin2025')
    CONTRASENA_ADMIN = os.getenv('CONTRASENA_ADMIN', 'pass2025')
    
    @staticmethod
    def verificar_configuracion():
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Verifica que las configuraciones críticas estén presentes
        Argumentos entrada: Ninguno
        Returns: 
            tuple: (bool exito, list errores)
        Modificaciones: Ninguna
        """
        errores = []
        
        if not os.path.exists(Configuracion.CREDENCIALES_GOOGLE):
            errores.append(
                f"No se encontró el archivo de credenciales de Google: "
                f"{Configuracion.CREDENCIALES_GOOGLE}"
            )
        
        if not Configuracion.IMAGGA_API_KEY or not Configuracion.IMAGGA_API_SECRET:
            errores.append("Faltan credenciales de Imagga API")
        
        if Configuracion.FLASK_ENV == 'produccion':
            if 'desarrollo' in Configuracion.SECRET_KEY:
                errores.append("SECRET_KEY de desarrollo detectada en producción")
            if 'desarrollo' in Configuracion.JWT_SECRET_KEY:
                errores.append("JWT_SECRET_KEY de desarrollo detectada en producción")
        
        return len(errores) == 0, errores


class ConfiguracionDesarrollo(Configuracion):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Configuración específica para entorno de desarrollo
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True


class ConfiguracionPruebas(Configuracion):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Configuración específica para tests unitarios
    """
    TESTING = True
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    WTF_CSRF_ENABLED = False
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


class ConfiguracionProduccion(Configuracion):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Configuración específica para entorno de producción
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    
    SECRET_KEY = os.getenv('CLAVE_SECRETA')
    JWT_SECRET_KEY = os.getenv('CLAVE_SECRETA_JWT')
    
    @staticmethod
    def verificar_produccion():
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Verificaciones adicionales para producción
        """
        assert ConfiguracionProduccion.SECRET_KEY, "CLAVE_SECRETA no configurada"
        assert ConfiguracionProduccion.JWT_SECRET_KEY, "CLAVE_SECRETA_JWT no configurada"
        assert 'desarrollo' not in ConfiguracionProduccion.SECRET_KEY.lower()
        assert 'desarrollo' not in ConfiguracionProduccion.JWT_SECRET_KEY.lower()


configuraciones = {
    'desarrollo': ConfiguracionDesarrollo,
    'pruebas': ConfiguracionPruebas,
    'produccion': ConfiguracionProduccion,
    'default': ConfiguracionDesarrollo
}


def obtener_configuracion(nombre_entorno=None):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Obtiene la configuración apropiada según el entorno
    Argumentos entrada:
        nombre_entorno (str): Nombre del entorno ('desarrollo', 'pruebas', 'produccion')
    Returns:
        Clase de configuración correspondiente
    Modificaciones: Ninguna
    """
    if nombre_entorno is None:
        nombre_entorno = os.getenv('FLASK_ENV', 'desarrollo')
    
    return configuraciones.get(nombre_entorno, ConfiguracionDesarrollo)
