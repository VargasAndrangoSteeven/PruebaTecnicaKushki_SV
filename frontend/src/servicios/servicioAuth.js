/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Servicio de autenticación
 */

import api from './api';

export const registrarUsuario = async (nombreUsuario, contrasena, captchaToken, captchaRespuesta) => {
  try {
    const respuesta = await api.post('/api/auth/registrar', {
      nombre_usuario: nombreUsuario,
      contrasena: contrasena,
      captcha_token: captchaToken,
      captcha_respuesta: captchaRespuesta
    });
    return respuesta.data;
  } catch (error) {
    return error.response?.data || { exito: false, mensaje: 'Error de conexión' };
  }
};

export const iniciarSesion = async (nombreUsuario, contrasena) => {
  try {
    const respuesta = await api.post('/api/auth/iniciar-sesion', {
      nombre_usuario: nombreUsuario,
      contrasena: contrasena
    });
    return respuesta.data;
  } catch (error) {
    return error.response?.data || { exito: false, mensaje: 'Error de conexión' };
  }
};

export const verificarToken = async () => {
  try {
    const respuesta = await api.get('/api/auth/verificar');
    return respuesta.data.exito;
  } catch (error) {
    return false;
  }
};
