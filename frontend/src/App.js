/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Componente principal de la aplicación
 */

import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Container } from '@mui/material';

import Login from './componentes/Autenticacion/Login';
import Registro from './componentes/Autenticacion/Registro';
import Analizador from './componentes/Analizador/Analizador';
import Historial from './componentes/Historial/Historial';
import Navbar from './componentes/Comunes/Navbar';

import { verificarToken } from './servicios/servicioAuth';

function App() {
  const [autenticado, setAutenticado] = useState(false);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    verificarAutenticacion();
  }, []);

  const verificarAutenticacion = async () => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      setCargando(false);
      return;
    }

    try {
      const valido = await verificarToken();
      setAutenticado(valido);
    } catch (error) {
      console.error('Error al verificar token:', error);
      localStorage.removeItem('token');
      setAutenticado(false);
    } finally {
      setCargando(false);
    }
  };

  const manejarLogin = () => {
    setAutenticado(true);
  };

  const manejarLogout = () => {
    localStorage.removeItem('token');
    setAutenticado(false);
  };

  if (cargando) {
    return <div>Cargando...</div>;
  }

  return (
    <>
      {autenticado && <Navbar alCerrarSesion={manejarLogout} />}
      
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          <Route 
            path="/login" 
            element={
              autenticado ? <Navigate to="/analizador" /> : <Login alIniciarSesion={manejarLogin} />
            } 
          />
          <Route 
            path="/registro" 
            element={
              autenticado ? <Navigate to="/analizador" /> : <Registro />
            } 
          />
          <Route 
            path="/analizador" 
            element={
              autenticado ? <Analizador /> : <Navigate to="/login" />
            } 
          />
          <Route 
            path="/historial" 
            element={
              autenticado ? <Historial /> : <Navigate to="/login" />
            } 
          />
          <Route path="/" element={<Navigate to={autenticado ? "/analizador" : "/login"} />} />
        </Routes>
      </Container>
    </>
  );
}

export default App;
