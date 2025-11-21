/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Componente de registro de usuario con captcha
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
import { registrarUsuario } from '../../servicios/servicioAuth';
import CaptchaMatematico from './CaptchaMatematico';
import './Login.css';

function Registro() {
  const [nombreUsuario, setNombreUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [confirmarContrasena, setConfirmarContrasena] = useState('');
  const [captchaToken, setCaptchaToken] = useState('');
  const [captchaRespuesta, setCaptchaRespuesta] = useState('');
  const [error, setError] = useState('');
  const [exito, setExito] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [mostrarContrasena, setMostrarContrasena] = useState(false);
  const [mostrarConfirmarContrasena, setMostrarConfirmarContrasena] = useState(false);
  const navigate = useNavigate();

  const manejarCaptcha = (token, respuesta) => {
    setCaptchaToken(token);
    setCaptchaRespuesta(respuesta);
    if (respuesta === '') {
      setError('');
    }
  };

  const manejarSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (contrasena !== confirmarContrasena) {
      setError('Las contraseñas no coinciden');
      return;
    }

    if (!captchaRespuesta || captchaRespuesta.trim() === '') {
      setError('Por favor completa el captcha');
      return;
    }

    if (!captchaToken) {
      setError('Error con el captcha. Por favor, genera uno nuevo haciendo clic en "Nuevo"');
      return;
    }

    setCargando(true);

    try {
      console.log('Enviando registro con:', {
        captchaToken,
        captchaRespuesta: captchaRespuesta.trim()
      });

      const respuesta = await registrarUsuario(
        nombreUsuario,
        contrasena,
        captchaToken,
        captchaRespuesta.trim()
      );

      console.log('Respuesta del servidor:', respuesta);

      if (respuesta.exito) {
        setExito(true);
        setTimeout(() => navigate('/login'), 2000);
      } else {
        const necesitaNuevoCaptcha =
          respuesta.mensaje.toLowerCase().includes('expirado') ||
          respuesta.mensaje.toLowerCase().includes('demasiados intentos') ||
          respuesta.mensaje.toLowerCase().includes('inválido');

        if (necesitaNuevoCaptcha) {
          setError('El captcha ha expirado o es inválido. Por favor, genera uno nuevo haciendo clic en "Nuevo"');
        } else {
          setError(respuesta.mensaje);
        }
      }
    } catch (err) {
      console.error('Error en registro:', err);
      setError('Error al registrar usuario');
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-fondo">
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
            Crear Cuenta
          </Typography>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          {exito && <Alert severity="success" sx={{ mb: 2 }}>¡Registro exitoso! Redirigiendo...</Alert>}

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
              helperText="Mínimo 8 caracteres, 1 mayúscula, 1 número, 1 símbolo (. , - _)"
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

            <TextField
              fullWidth
              label="Confirmar Contraseña"
              type={mostrarConfirmarContrasena ? 'text' : 'password'}
              value={confirmarContrasena}
              onChange={(e) => setConfirmarContrasena(e.target.value)}
              margin="normal"
              required
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle confirm password visibility"
                      onClick={() => setMostrarConfirmarContrasena(!mostrarConfirmarContrasena)}
                      onMouseDown={(e) => e.preventDefault()}
                      edge="end"
                      sx={{
                        color: '#1976d2',
                        '&:hover': {
                          background: 'rgba(25, 118, 210, 0.08)'
                        }
                      }}
                    >
                      {mostrarConfirmarContrasena ? <VisibilityOff /> : <Visibility />}
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

            <Box sx={{ my: 3 }}>
              <CaptchaMatematico onCaptchaValido={manejarCaptcha} />
            </Box>

            <Button
              fullWidth
              type="submit"
              variant="contained"
              size="large"
              disabled={cargando || !captchaRespuesta}
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
              {cargando ? 'Registrando...' : 'Registrarse'}
            </Button>

            <Typography align="center">
              ¿Ya tienes cuenta?{' '}
              <Link to="/login" style={{ textDecoration: 'none', color: '#1976d2', fontWeight: 500 }}>
                Inicia sesión aquí
              </Link>
            </Typography>
          </Box>
        </Paper>
      </Container>
    </div>
  );
}

export default Registro;
