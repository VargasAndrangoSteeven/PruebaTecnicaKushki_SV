"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Modelo de base de datos para Análisis de Imágenes.
             Almacena resultados de análisis de IA.
"""

from datetime import datetime
import json
from . import db


class Analisis(db.Model):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Modelo de Análisis de Imagen
    """
    
    __tablename__ = 'analisis'
    
    id = db.Column(db.String(36), primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)
    proveedor_ia = db.Column(db.String(50), nullable=False)
    etiquetas_json = db.Column(db.Text, nullable=False)
    fecha_analisis = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __init__(self, id, usuario_id, nombre_archivo, ruta_archivo, proveedor_ia, etiquetas):
        """Constructor del modelo Análisis"""
        self.id = id
        self.usuario_id = usuario_id
        self.nombre_archivo = nombre_archivo
        self.ruta_archivo = ruta_archivo
        self.proveedor_ia = proveedor_ia
        self.establecer_etiquetas(etiquetas)
    
    def establecer_etiquetas(self, etiquetas):
        """Convierte etiquetas a JSON y las almacena"""
        self.etiquetas_json = json.dumps(etiquetas, ensure_ascii=False)
    
    def obtener_etiquetas(self):
        """Obtiene las etiquetas como lista de diccionarios"""
        return json.loads(self.etiquetas_json)
    
    def a_dict(self):
        """Convierte el análisis a diccionario"""
        return {
            'id': self.id,
            'nombre_archivo': self.nombre_archivo,
            'proveedor_ia': self.proveedor_ia,
            'etiquetas': self.obtener_etiquetas(),
            'fecha_analisis': self.fecha_analisis.isoformat()
        }
    
    def __repr__(self):
        return f'<Analisis {self.id} - {self.nombre_archivo}>'
