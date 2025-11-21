/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Configuración de Axios para peticiones HTTP
 */

import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'https://localhost:5001';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default api;
