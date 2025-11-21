/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Componente de inicio de sesión
 */

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  IconButton,
  InputAdornment
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { iniciarSesion } from '../../servicios/servicioAuth';
import ModalBienvenida from '../Comunes/ModalBienvenida';
import './Login.css';

function Login({ alIniciarSesion }) {
  const [nombreUsuario, setNombreUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [error, setError] = useState('');
  const [cargando, setCargando] = useState(false);
  const [mostrarModalBienvenida, setMostrarModalBienvenida] = useState(false);
  const [mostrarContrasena, setMostrarContrasena] = useState(false);
  const navigate = useNavigate();

  const manejarSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setCargando(true);

    try {
      const respuesta = await iniciarSesion(nombreUsuario, contrasena);

      if (respuesta.exito) {
        localStorage.setItem('token', respuesta.datos.token);

        const usuarioId = respuesta.datos.usuario.id;
        const modalVisto = localStorage.getItem(`modal_bienvenida_${usuarioId}`);

        if (!modalVisto) {
          localStorage.setItem(`modal_bienvenida_${usuarioId}`, 'true');
          setMostrarModalBienvenida(true);
        } else {
          alIniciarSesion();
          navigate('/analizador');
        }
      } else {
        setError(respuesta.mensaje);
      }
    } catch (err) {
      setError('Error al iniciar sesión. Por favor, intenta nuevamente.');
    } finally {
      setCargando(false);
    }
  };

  const cerrarModalBienvenida = () => {
    setMostrarModalBienvenida(false);
    alIniciarSesion();
    navigate('/analizador');
  };

  return (
    <div className="login-fondo">
      {/* Modal de Bienvenida */}
      <ModalBienvenida
        abierto={mostrarModalBienvenida}
        alCerrar={cerrarModalBienvenida}
      />

      {/* Partículas animadas */}
      <div className="particulas">
        {[...Array(20)].map((_, i) => (
          <div key={i} className="particula"></div>
        ))}
      </div>

      <Container maxWidth="sm" sx={{ position: 'relative', zIndex: 1 }}>
        <Paper
          elevation={6}
          sx={{
            p: 4,
            mt: 8,
            background: 'rgba(255, 255, 255, 0.95)',
            borderRadius: 3,
            backdropFilter: 'blur(10px)'
          }}
        >
          <Typography variant="h4" align="center" gutterBottom sx={{ fontWeight: 600, color: '#1a237e' }}>
            Iniciar Sesión
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={manejarSubmit}>
            <TextField
              fullWidth
              label="Usuario"
              value={nombreUsuario}
              onChange={(e) => setNombreUsuario(e.target.value)}
              margin="normal"
              required
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2
                }
              }}
            />

            <TextField
              fullWidth
              label="Contraseña"
              type={mostrarContrasena ? 'text' : 'password'}
              value={contrasena}
              onChange={(e) => setContrasena(e.target.value)}
              margin="normal"
              required
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={() => setMostrarContrasena(!mostrarContrasena)}
                      onMouseDown={(e) => e.preventDefault()}
                      edge="end"
                      sx={{
                        color: '#1976d2',
                        '&:hover': {
                          background: 'rgba(25, 118, 210, 0.08)'
                        }
                      }}
                    >
                      {mostrarContrasena ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                )
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: 2
                }
              }}
            />

            <Button
              fullWidth
              type="submit"
              variant="contained"
              size="large"
              disabled={cargando}
              sx={{
                mt: 3,
                mb: 2,
                borderRadius: 2,
                py: 1.5,
                background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #1565c0 30%, #1976d2 90%)'
                }
              }}
            >
              {cargando ? 'Iniciando...' : 'Iniciar Sesión'}
            </Button>

            <Typography align="center">
              ¿No tienes cuenta?{' '}
              <Link to="/registro" style={{ textDecoration: 'none', color: '#1976d2', fontWeight: 500 }}>
                Regístrate aquí
              </Link>
            </Typography>
          </Box>
        </Paper>
      </Container>
    </div>
  );
}

export default Login;
