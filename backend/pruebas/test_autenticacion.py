"""
Autor: Steeven Vargas
Fecha: Noviembre 2024
Descripción: Tests unitarios para el módulo de autenticación
"""

import pytest
from modelos import Usuario


class TestRegistro:
    """Tests para el endpoint de registro"""
    
    def test_registro_exitoso(self, cliente):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Test de registro exitoso de usuario
        """
        respuesta = cliente.post('/api/auth/registrar', json={
            'nombre_usuario': 'nuevo_usuario',
            'contrasena': 'NuevaPass123!'
        })
        
        assert respuesta.status_code == 201
        datos = respuesta.get_json()
        assert datos['exito'] is True
        assert 'datos' in datos
        assert datos['datos']['nombre_usuario'] == 'nuevo_usuario'
    
    def test_registro_contrasena_debil(self, cliente):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Test de registro con contraseña débil
        """
        respuesta = cliente.post('/api/auth/registrar', json={
            'nombre_usuario': 'usuario_test',
            'contrasena': '123'
        })
        
        assert respuesta.status_code == 400
        datos = respuesta.get_json()
        assert datos['exito'] is False
    
    def test_registro_usuario_duplicado(self, cliente, usuario_prueba):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Test de registro con usuario ya existente
        """
        respuesta = cliente.post('/api/auth/registrar', json={
            'nombre_usuario': 'usuario_test',
            'contrasena': 'OtraPass123!'
        })
        
        assert respuesta.status_code == 400
        datos = respuesta.get_json()
        assert datos['exito'] is False
        assert 'ya está en uso' in datos['mensaje']


class TestInicioSesion:
    """Tests para el endpoint de inicio de sesión"""
    
    def test_inicio_sesion_exitoso(self, cliente, usuario_prueba):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Test de inicio de sesión exitoso
        """
        respuesta = cliente.post('/api/auth/iniciar-sesion', json={
            'nombre_usuario': 'usuario_test',
            'contrasena': 'TestPass123!'
        })
        
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos['exito'] is True
        assert 'token' in datos['datos']
        assert 'usuario' in datos['datos']
    
    def test_inicio_sesion_contrasena_incorrecta(self, cliente, usuario_prueba):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Test de inicio de sesión con contraseña incorrecta
        """
        respuesta = cliente.post('/api/auth/iniciar-sesion', json={
            'nombre_usuario': 'usuario_test',
            'contrasena': 'ContrasenaIncorrecta123!'
        })
        
        assert respuesta.status_code == 401
        datos = respuesta.get_json()
        assert datos['exito'] is False
    
    def test_inicio_sesion_usuario_no_existe(self, cliente):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Test de inicio de sesión con usuario inexistente
        """
        respuesta = cliente.post('/api/auth/iniciar-sesion', json={
            'nombre_usuario': 'usuario_no_existe',
            'contrasena': 'Pass123!'
        })
        
        assert respuesta.status_code == 401
        datos = respuesta.get_json()
        assert datos['exito'] is False


class TestVerificacionToken:
    """Tests para el endpoint de verificación de token"""
    
    def test_verificar_token_valido(self, cliente, headers_autenticados):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Test de verificación de token válido
        """
        respuesta = cliente.get('/api/auth/verificar', headers=headers_autenticados)
        
        assert respuesta.status_code == 200
        datos = respuesta.get_json()
        assert datos['exito'] is True
    
    def test_verificar_token_sin_token(self, cliente):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Test de verificación sin token
        """
        respuesta = cliente.get('/api/auth/verificar')
        
        assert respuesta.status_code == 401
    
    def test_verificar_token_invalido(self, cliente):
        """
        Autor: Steeven Vargas
        Fecha: Noviembre 2024
        Descripción: Test de verificación con token inválido
        """
        headers = {
            'Authorization': 'Bearer token_invalido_123456789'
        }
        respuesta = cliente.get('/api/auth/verificar', headers=headers)
        
        assert respuesta.status_code == 422  # Unprocessable Entity
