"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Servicio de encriptación con GPG
"""

import gnupg
import os
from flask import current_app


class ServicioEncriptacion:
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Gestión de encriptación con GPG
    """
    
    def __init__(self):
        """Constructor del servicio de encriptación"""
        self.gpg = gnupg.GPG()
        self.frase_seguridad = current_app.config.get('FRASE_SEGURIDAD_GPG', 'desarrollo')
    
    def encriptar_datos(self, datos):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Encripta datos con GPG
        Argumentos entrada:
            datos (str): Datos a encriptar
        Returns:
            str: Datos encriptados
        Modificaciones: Ninguna
        """
        try:
            encriptado = self.gpg.encrypt(
                datos,
                recipients=None,
                symmetric=True,
                passphrase=self.frase_seguridad
            )
            return str(encriptado)
        except Exception as e:
            raise Exception(f"Error al encriptar: {str(e)}")
    
    def desencriptar_datos(self, datos_encriptados):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Desencripta datos con GPG
        Argumentos entrada:
            datos_encriptados (str): Datos encriptados
        Returns:
            str: Datos desencriptados
        Modificaciones: Ninguna
        """
        try:
            desencriptado = self.gpg.decrypt(
                datos_encriptados,
                passphrase=self.frase_seguridad
            )
            return str(desencriptado)
        except Exception as e:
            raise Exception(f"Error al desencriptar: {str(e)}")
