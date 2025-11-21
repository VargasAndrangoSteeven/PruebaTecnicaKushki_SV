"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Servicio para traducir e interpretar resultados de análisis de IA
"""

import requests
from deep_translator import GoogleTranslator


class ServicioInterpretacion:
    """
    Servicio para traducir etiquetas y generar interpretaciones de resultados
    """

    @staticmethod
    def traducir_etiquetas(etiquetas):
        """
        Traduce una lista de etiquetas de inglés a español

        Args:
            etiquetas (list): Lista de dicts con 'etiqueta' y 'confianza'

        Returns:
            list: Lista de etiquetas traducidas
        """
        try:
            translator = GoogleTranslator(source='en', target='es')
            etiquetas_traducidas = []

            for etiqueta in etiquetas:
                try:
                    confianza_porcentaje = int(etiqueta['confianza'] * 100)

                    nombre_traducido = translator.translate(etiqueta['etiqueta'])
                    etiquetas_traducidas.append({
                        'nombre': nombre_traducido.capitalize(),
                        'nombre_original': etiqueta['etiqueta'],
                        'confianza': confianza_porcentaje
                    })
                except Exception as e:
                    confianza_porcentaje = int(etiqueta['confianza'] * 100)
                    etiquetas_traducidas.append({
                        'nombre': etiqueta['etiqueta'].capitalize(),
                        'nombre_original': etiqueta['etiqueta'],
                        'confianza': confianza_porcentaje
                    })

            return etiquetas_traducidas

        except Exception as e:
            return [{
                'nombre': etiqueta['etiqueta'].capitalize(),
                'nombre_original': etiqueta['etiqueta'],
                'confianza': int(etiqueta['confianza'] * 100)
            } for etiqueta in etiquetas]

    @staticmethod
    def generar_interpretacion(proveedor, etiquetas_traducidas):
        """
        Genera una interpretación en lenguaje natural de los resultados

        Args:
            proveedor (str): Nombre del proveedor de IA (google o imagga)
            etiquetas_traducidas (list): Lista de etiquetas traducidas con confianza

        Returns:
            str: Texto interpretativo
        """
        if not etiquetas_traducidas:
            return f"Según el modelo {proveedor.upper()}, no se detectaron elementos en la imagen."

        principal = etiquetas_traducidas[0]
        confianza_principal = int(principal['confianza'])

        nombre_proveedor = {
            'google': 'Google Cloud Vision',
            'imagga': 'Imagga'
        }.get(proveedor.lower(), proveedor.upper())

        interpretacion = f"Según el modelo {nombre_proveedor}, con un {confianza_principal}% de confianza "
        interpretacion += f"se identifica como **{principal['nombre']}**"

        if len(etiquetas_traducidas) > 1:
            secundarias = etiquetas_traducidas[1:min(4, len(etiquetas_traducidas))]
            nombres_secundarios = [
                f"{et['nombre']} ({int(et['confianza'])}%)"
                for et in secundarias
            ]

            if len(nombres_secundarios) == 1:
                interpretacion += f", con similitudes a {nombres_secundarios[0]}"
            else:
                interpretacion += f", con similitudes a {', '.join(nombres_secundarios[:-1])} y {nombres_secundarios[-1]}"

        interpretacion += "."

        return interpretacion

    @staticmethod
    def procesar_resultados(proveedor, etiquetas):
        """
        Procesa los resultados completos: traduce e interpreta

        Args:
            proveedor (str): Nombre del proveedor de IA
            etiquetas (list): Lista de etiquetas originales

        Returns:
            dict: Resultados procesados con traducción e interpretación
        """
        etiquetas_traducidas = ServicioInterpretacion.traducir_etiquetas(etiquetas)

        interpretacion = ServicioInterpretacion.generar_interpretacion(
            proveedor,
            etiquetas_traducidas
        )

        return {
            'etiquetas': etiquetas_traducidas,
            'interpretacion': interpretacion,
            'total_etiquetas': len(etiquetas_traducidas)
        }
