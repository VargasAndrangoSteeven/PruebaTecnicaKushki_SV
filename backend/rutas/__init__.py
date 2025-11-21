"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Módulo de rutas (endpoints) del backend
"""

from .autenticacion import autenticacion_bp
from .analisis import analisis_bp

__all__ = ['autenticacion_bp', 'analisis_bp']
