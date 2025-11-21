"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Rutas para análisis de imágenes con IA
"""

import os
import uuid
from flask import Blueprint, request, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime

from modelos import db, Usuario, Analisis
from servicios.servicio_ia import ServicioIA
from servicios.servicio_interpretacion import ServicioInterpretacion
from utilidades.respuestas import respuesta_exitosa, respuesta_error, respuesta_no_encontrado
from utilidades.validadores import es_imagen_valida
from config.seguridad import limitar_peticiones

analisis_bp = Blueprint('analisis', __name__)


@analisis_bp.route('/analizar', methods=['POST'])
@jwt_required()
@limitar_peticiones(limite_por_minuto=10)
def analizar_imagen():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para analizar una imagen con IA
    """
    try:
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(int(usuario_id))

        if not usuario:
            return respuesta_error("Usuario no encontrado", codigo=404)
        
        if 'imagen' not in request.files:
            return respuesta_error("No se proporcionó ninguna imagen")
        
        archivo = request.files['imagen']
        
        if archivo.filename == '':
            return respuesta_error("No se seleccionó ningún archivo")
        
        valida, mensaje = es_imagen_valida(archivo)
        if not valida:
            return respuesta_error(mensaje)
        
        proveedor = request.form.get('tipo_ia') or request.form.get('proveedor_ia', 'google')
        proveedor = proveedor.lower()
        if proveedor not in ['google', 'imagga']:
            return respuesta_error("Proveedor no válido. Use 'google' o 'imagga'")
        
        nombre_archivo = secure_filename(archivo.filename)
        extension = nombre_archivo.rsplit('.', 1)[1].lower()
        nombre_unico = f"{uuid.uuid4().hex}.{extension}"
        
        directorio_usuario = os.path.join(
            current_app.config['DIRECTORIO_CARGAS'],
            str(usuario_id)
        )
        os.makedirs(directorio_usuario, exist_ok=True)
        
        ruta_archivo = os.path.join(directorio_usuario, nombre_unico)
        archivo.save(ruta_archivo)
        
        try:
            etiquetas = ServicioIA.analizar_imagen(ruta_archivo, proveedor)
        except Exception as e:
            if os.path.exists(ruta_archivo):
                os.remove(ruta_archivo)
            return respuesta_error(f"Error al analizar imagen: {str(e)}", codigo=500)

        try:
            resultados_procesados = ServicioInterpretacion.procesar_resultados(
                proveedor,
                etiquetas
            )
        except Exception as e:
            resultados_procesados = {
                'etiquetas': etiquetas,
                'interpretacion': None,
                'total_etiquetas': len(etiquetas)
            }

        id_analisis = str(uuid.uuid4())
        nuevo_analisis = Analisis(
            id=id_analisis,
            usuario_id=usuario_id,
            nombre_archivo=nombre_archivo,
            ruta_archivo=ruta_archivo,
            proveedor_ia=proveedor,
            etiquetas=etiquetas
        )

        db.session.add(nuevo_analisis)
        db.session.commit()

        respuesta_datos = nuevo_analisis.a_dict()
        respuesta_datos['etiquetas_traducidas'] = resultados_procesados['etiquetas']
        respuesta_datos['interpretacion'] = resultados_procesados['interpretacion']

        return respuesta_exitosa(
            datos=respuesta_datos,
            mensaje="Imagen analizada exitosamente",
            codigo=201
        )
        
    except Exception as e:
        db.session.rollback()
        return respuesta_error(f"Error al procesar imagen: {str(e)}", codigo=500)


@analisis_bp.route('/historial', methods=['GET'])
@jwt_required()
def obtener_historial():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para obtener historial de análisis del usuario
    """
    try:
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(int(usuario_id))

        if not usuario:
            return respuesta_error("Usuario no encontrado", codigo=404)
        
        pagina = request.args.get('pagina', 1, type=int)
        por_pagina = request.args.get('por_pagina', 20, type=int)
        
        por_pagina = min(por_pagina, 100)
        
        paginacion = Analisis.query.filter_by(usuario_id=usuario_id)\
            .order_by(Analisis.fecha_analisis.desc())\
            .paginate(page=pagina, per_page=por_pagina, error_out=False)
        
        analisis_lista = [analisis.a_dict() for analisis in paginacion.items]
        
        return respuesta_exitosa(
            datos={
                'analisis': analisis_lista,
                'total': paginacion.total,
                'pagina_actual': paginacion.page,
                'total_paginas': paginacion.pages,
                'por_pagina': paginacion.per_page
            },
            mensaje=f"Se encontraron {paginacion.total} análisis"
        )
        
    except Exception as e:
        return respuesta_error(f"Error al obtener historial: {str(e)}", codigo=500)


@analisis_bp.route('/historial/<string:id_analisis>', methods=['GET'])
@jwt_required()
def obtener_analisis(id_analisis):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para obtener un análisis específico
    """
    try:
        usuario_id = get_jwt_identity()

        analisis = Analisis.query.filter_by(
            id=id_analisis,
            usuario_id=usuario_id
        ).first()

        if not analisis:
            return respuesta_no_encontrado("Análisis no encontrado")

        datos_analisis = analisis.a_dict()

        try:
            etiquetas = analisis.obtener_etiquetas()
            resultados_procesados = ServicioInterpretacion.procesar_resultados(
                analisis.proveedor_ia,
                etiquetas
            )
            datos_analisis['etiquetas_traducidas'] = resultados_procesados['etiquetas']
            datos_analisis['interpretacion'] = resultados_procesados['interpretacion']
        except Exception as e:
            datos_analisis['etiquetas_traducidas'] = None
            datos_analisis['interpretacion'] = None

        return respuesta_exitosa(
            datos=datos_analisis,
            mensaje="Análisis encontrado"
        )

    except Exception as e:
        return respuesta_error(f"Error al obtener análisis: {str(e)}", codigo=500)


@analisis_bp.route('/historial/<string:id_analisis>/imagen', methods=['GET'])
@jwt_required()
def obtener_imagen_analisis(id_analisis):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para descargar la imagen de un análisis
    """
    try:
        usuario_id = get_jwt_identity()
        
        analisis = Analisis.query.filter_by(
            id=id_analisis,
            usuario_id=usuario_id
        ).first()
        
        if not analisis:
            return respuesta_no_encontrado("Análisis no encontrado")
        
        if not os.path.exists(analisis.ruta_archivo):
            return respuesta_error("Archivo no encontrado en el servidor", codigo=404)
        
        return send_file(
            analisis.ruta_archivo,
            as_attachment=True,
            download_name=analisis.nombre_archivo
        )
        
    except Exception as e:
        return respuesta_error(f"Error al obtener imagen: {str(e)}", codigo=500)


@analisis_bp.route('/historial/<string:id_analisis>', methods=['DELETE'])
@jwt_required()
def eliminar_analisis(id_analisis):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Endpoint para eliminar un análisis
    """
    try:
        usuario_id = get_jwt_identity()
        
        analisis = Analisis.query.filter_by(
            id=id_analisis,
            usuario_id=usuario_id
        ).first()
        
        if not analisis:
            return respuesta_no_encontrado("Análisis no encontrado")
        
        if os.path.exists(analisis.ruta_archivo):
            os.remove(analisis.ruta_archivo)
        
        db.session.delete(analisis)
        db.session.commit()
        
        return respuesta_exitosa(
            mensaje="Análisis eliminado exitosamente"
        )
        
    except Exception as e:
        db.session.rollback()
        return respuesta_error(f"Error al eliminar análisis: {str(e)}", codigo=500)
