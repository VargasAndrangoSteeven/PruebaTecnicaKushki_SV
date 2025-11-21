"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Módulo de configuración del backend.
             Exporta las configuraciones principales.
"""

from .configuracion import (
    Configuracion,
    ConfiguracionDesarrollo,
    ConfiguracionPruebas,
    ConfiguracionProduccion,
    obtener_configuracion,
    configuraciones
)

from .seguridad import (
    configurar_headers_seguridad,
    generar_clave_segura
)

__all__ = [
    'Configuracion',
    'ConfiguracionDesarrollo',
    'ConfiguracionPruebas',
    'ConfiguracionProduccion',
    'obtener_configuracion',
    'configuraciones',
    'configurar_headers_seguridad',
    'generar_clave_segura'
]
