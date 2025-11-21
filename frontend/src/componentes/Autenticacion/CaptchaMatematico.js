/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Componente de captcha matemático local
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Typography,
  Button,
  Paper,
  CircularProgress
} from '@mui/material';
import { Refresh } from '@mui/icons-material';
import api from '../../servicios/api';

function CaptchaMatematico({ onCaptchaValido }) {
  const [captcha, setCaptcha] = useState(null);
  const [respuesta, setRespuesta] = useState('');
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    cargarCaptcha();
  }, []);

  const cargarCaptcha = async () => {
    setCargando(true);
    setError('');
    setRespuesta('');

    try {
      console.log('Solicitando nuevo captcha...');
      const response = await api.get('/api/auth/captcha');

      console.log('Respuesta del servidor:', response.data);

      if (response.data.exito) {
        setCaptcha(response.data.datos);
        console.log('Nuevo token de captcha:', response.data.datos.token);
        onCaptchaValido(response.data.datos.token, '');
      } else {
        setError('Error al cargar captcha');
      }
    } catch (err) {
      console.error('Error al cargar captcha:', err);
      setError('Error de conexión');
    } finally {
      setCargando(false);
    }
  };

  const manejarCambioRespuesta = (e) => {
    const valor = e.target.value;
    setRespuesta(valor);
    if (captcha && captcha.token) {
      console.log('Captcha respuesta actualizada:', valor);
      onCaptchaValido(captcha.token, valor);
    }
  };

  if (cargando) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={2}>
        <CircularProgress size={24} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Typography color="error" sx={{ mb: 2 }}>{error}</Typography>
        <Button
          onClick={cargarCaptcha}
          startIcon={<Refresh />}
          variant="contained"
          sx={{
            borderRadius: 2,
            background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #1565c0 30%, #1976d2 90%)'
            }
          }}
        >
          Reintentar
        </Button>
      </Box>
    );
  }

  return (
    <Paper
      elevation={2}
      sx={{
        p: 2,
        backgroundColor: '#f5f5f5',
        border: '1px solid #ddd'
      }}
    >
      <Box>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
          <Box flex={1}>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Verifica que eres humano:
            </Typography>
            <Typography variant="h6" color="primary">
              {captcha?.pregunta}
            </Typography>
          </Box>

          <Button
            onClick={cargarCaptcha}
            size="small"
            startIcon={<Refresh />}
            title="Generar nuevo captcha"
            variant="contained"
            sx={{
              borderRadius: 2,
              background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #1565c0 30%, #1976d2 90%)'
              }
            }}
          >
            Nuevo
          </Button>
        </Box>

        <TextField
          fullWidth
          type="number"
          label="Tu respuesta"
          placeholder="Ingresa el resultado"
          value={respuesta}
          onChange={manejarCambioRespuesta}
          size="small"
          inputProps={{
            min: 0,
            style: { textAlign: 'center' }
          }}
        />
      </Box>
    </Paper>
  );
}

export default CaptchaMatematico;
