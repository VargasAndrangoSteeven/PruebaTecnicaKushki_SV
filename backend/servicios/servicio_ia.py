"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Servicio para integración con APIs de IA (Google Vision, Imagga)
Argumentos entrada: Varía según método
Returns: Resultados de análisis de IA
Modificaciones: Ninguna
"""

import os
import base64
import requests
from google.cloud import vision
from flask import current_app


class ServicioIA:
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Clase para gestionar análisis de imágenes con IA
    """
    
    @staticmethod
    def analizar_con_google(ruta_imagen):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Analiza imagen usando Google Cloud Vision API
        Argumentos entrada:
            ruta_imagen (str): Ruta al archivo de imagen
        Returns:
            list: Lista de etiquetas con confianza
        Modificaciones: Ninguna
        """
        try:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = current_app.config['CREDENCIALES_GOOGLE']
            
            cliente = vision.ImageAnnotatorClient()
            
            with open(ruta_imagen, 'rb') as archivo_imagen:
                contenido = archivo_imagen.read()
            
            imagen = vision.Image(content=contenido)
            
            respuesta = cliente.label_detection(image=imagen, max_results=10)
            etiquetas_raw = respuesta.label_annotations
            
            etiquetas = []
            for etiqueta in etiquetas_raw:
                etiquetas.append({
                    'etiqueta': etiqueta.description,
                    'confianza': round(etiqueta.score, 2)
                })
            
            return etiquetas
            
        except Exception as e:
            raise Exception(f"Error al analizar con Google Vision: {str(e)}")
    
    @staticmethod
    def analizar_con_imagga(ruta_imagen):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Analiza imagen usando Imagga API
        Argumentos entrada:
            ruta_imagen (str): Ruta al archivo de imagen
        Returns:
            list: Lista de etiquetas con confianza
        Modificaciones: Ninguna
        """
        try:
            api_key = current_app.config['IMAGGA_API_KEY']
            api_secret = current_app.config['IMAGGA_API_SECRET']
            endpoint = current_app.config['IMAGGA_ENDPOINT']
            
            with open(ruta_imagen, 'rb') as archivo_imagen:
                contenido_imagen = base64.b64encode(archivo_imagen.read()).decode('utf-8')
            
            headers = {
                'Authorization': f'Basic {base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()}'
            }
            
            datos = {
                'image_base64': contenido_imagen
            }
            
            respuesta = requests.post(endpoint, headers=headers, data=datos, timeout=30)
            respuesta.raise_for_status()
            
            resultado = respuesta.json()
            
            etiquetas = []
            if 'result' in resultado and 'tags' in resultado['result']:
                for tag in resultado['result']['tags'][:10]:
                    etiquetas.append({
                        'etiqueta': tag['tag']['es'] if 'es' in tag['tag'] else tag['tag']['en'],
                        'confianza': round(tag['confidence'] / 100, 2)
                    })
            
            return etiquetas
            
        except Exception as e:
            raise Exception(f"Error al analizar con Imagga: {str(e)}")
    
    @staticmethod
    def analizar_imagen(ruta_imagen, proveedor='google'):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Analiza imagen con el proveedor especificado
        Argumentos entrada:
            ruta_imagen (str): Ruta al archivo de imagen
            proveedor (str): 'google' o 'imagga'
        Returns:
            list: Lista de etiquetas con confianza
        Modificaciones: Ninguna
        """
        if proveedor == 'google':
            return ServicioIA.analizar_con_google(ruta_imagen)
        elif proveedor == 'imagga':
            return ServicioIA.analizar_con_imagga(ruta_imagen)
        else:
            raise ValueError(f"Proveedor no válido: {proveedor}. Use 'google' o 'imagga'")
