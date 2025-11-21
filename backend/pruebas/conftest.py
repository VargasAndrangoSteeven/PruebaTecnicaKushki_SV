"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Configuración de pytest para tests del backend
"""

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import crear_aplicacion
from modelos import db, Usuario
from config.configuracion import ConfiguracionPruebas


@pytest.fixture(scope='function')
def app():
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Fixture que crea una aplicación para tests
    """
    app = crear_aplicacion(ConfiguracionPruebas)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def cliente(app):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Fixture que crea un cliente de prueba
    """
    return app.test_client()


@pytest.fixture(scope='function')
def usuario_prueba(app):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Fixture que crea un usuario de prueba
    """
    with app.app_context():
        usuario = Usuario(
            nombre_usuario='usuario_test',
            contrasena='TestPass123!'
        )
        db.session.add(usuario)
        db.session.commit()
        
        db.session.refresh(usuario)
        
        return usuario


@pytest.fixture(scope='function')
def token_autenticacion(cliente, usuario_prueba):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Fixture que genera un token JWT para tests
    """
    respuesta = cliente.post('/api/auth/iniciar-sesion', json={
        'nombre_usuario': 'usuario_test',
        'contrasena': 'TestPass123!'
    })
    
    datos = respuesta.get_json()
    return datos['datos']['token']


@pytest.fixture(scope='function')
def headers_autenticados(token_autenticacion):
    """
    Autor: Steeven Vargas
    Fecha: Noviembre 2024
    Descripción: Fixture que retorna headers con token JWT
    """
    return {
        'Authorization': f'Bearer {token_autenticacion}',
        'Content-Type': 'application/json'
    }
