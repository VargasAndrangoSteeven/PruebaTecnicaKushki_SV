/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Componente principal del analizador de imágenes
 */

import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  LinearProgress
} from '@mui/material';
import { CloudUpload, Image } from '@mui/icons-material';

function Analizador() {
  const [imagen, setImagen] = useState(null);
  const [proveedorIA, setProveedorIA] = useState('google');
  const [analizando, setAnalizando] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState('');

  const manejarSeleccionImagen = (e) => {
    const archivo = e.target.files[0];
    if (archivo) {
      setImagen(archivo);
      setResultado(null);
      setError('');
    }
  };

  const manejarAnalizar = async () => {
    if (!imagen) {
      setError('Por favor selecciona una imagen');
      return;
    }

    setAnalizando(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('imagen', imagen);
      formData.append('proveedor_ia', proveedorIA);

      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/analizar`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      const data = await response.json();

      if (data.exito) {
        setResultado(data.datos);
      } else {
        setError(data.mensaje);
      }
    } catch (err) {
      setError('Error al analizar la imagen');
    } finally {
      setAnalizando(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Paper
        elevation={6}
        sx={{
          p: 4,
          mt: 4,
          background: 'rgba(255, 255, 255, 0.95)',
          borderRadius: 3,
          backdropFilter: 'blur(10px)'
        }}
      >
        <Typography variant="h4" gutterBottom align="center" sx={{ fontWeight: 600, color: '#ffffffff' }}>
          Analizador de Imágenes
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <Box sx={{ mb: 3 }}>
          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>Proveedor de IA</InputLabel>
            <Select
              value={proveedorIA}
              label="Proveedor de IA"
              onChange={(e) => {
                setProveedorIA(e.target.value);
                setResultado(null);
              }}
            >
              <MenuItem value="google">Google Cloud Vision</MenuItem>
              <MenuItem value="imagga">Imagga</MenuItem>
            </Select>
          </FormControl>

          <Button
            variant="contained"
            component="label"
            startIcon={<CloudUpload />}
            fullWidth
            sx={{
              borderRadius: 2,
              color: '#ffffff',
              background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #1565c0 30%, #1976d2 90%)'
              }
            }}
          >
            Seleccionar Imagen
            <input
              type="file"
              hidden
              accept="image/*"
              onChange={manejarSeleccionImagen}
            />
          </Button>

          {imagen && (
            <Typography sx={{ mt: 2 }}>
              Imagen seleccionada: {imagen.name}
            </Typography>
          )}
        </Box>

        <Button
          variant="contained"
          color="primary"
          fullWidth
          size="large"
          onClick={manejarAnalizar}
          disabled={!imagen || analizando}
          startIcon={analizando ? <CircularProgress size={20} sx={{ color: '#ffffff' }} /> : <Image />}
          sx={{
            borderRadius: 2,
            py: 1.5,
            color: '#ffffff',
            background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #1565c0 30%, #1976d2 90%)'
            }
          }}
        >
          {analizando ? 'Analizando...' : 'Analizar Imagen'}
        </Button>

        {resultado && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Resultados del Análisis:
            </Typography>

            {resultado.interpretacion && (
              <Alert severity="info" sx={{ mb: 3 }}>
                <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                  {resultado.interpretacion}
                </Typography>
              </Alert>
            )}

            <Typography variant="subtitle1" gutterBottom sx={{ mt: 2, fontWeight: 'bold' }}>
              Etiquetas Detectadas:
            </Typography>

            {resultado.etiquetas_traducidas && resultado.etiquetas_traducidas.length > 0 ? (
              resultado.etiquetas_traducidas.map((etiqueta, index) => (
                <Box key={index} sx={{ mb: 2.5 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
                    <Typography>
                      <strong>{etiqueta.nombre}</strong> <span style={{ color: '#666', fontSize: '0.9em' }}>({etiqueta.nombre_original})</span>
                    </Typography>
                    <Typography color="primary" sx={{ fontWeight: 'bold' }}>
                      {etiqueta.confianza}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={etiqueta.confianza}
                    sx={{
                      height: 8,
                      borderRadius: 1,
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        borderRadius: 1,
                        backgroundColor: etiqueta.confianza >= 80 ? '#4caf50' : etiqueta.confianza >= 60 ? '#ff9800' : '#f44336'
                      }
                    }}
                  />
                </Box>
              ))
            ) : (
              resultado.etiquetas.map((etiqueta, index) => (
                <Box key={index} sx={{ mb: 2.5 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
                    <Typography>
                      {etiqueta.etiqueta}
                    </Typography>
                    <Typography color="primary" sx={{ fontWeight: 'bold' }}>
                      {(etiqueta.confianza * 100).toFixed(0)}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={etiqueta.confianza * 100}
                    sx={{
                      height: 8,
                      borderRadius: 1,
                      backgroundColor: '#e0e0e0',
                      '& .MuiLinearProgress-bar': {
                        borderRadius: 1,
                        backgroundColor: (etiqueta.confianza * 100) >= 80 ? '#4caf50' : (etiqueta.confianza * 100) >= 60 ? '#ff9800' : '#f44336'
                      }
                    }}
                  />
                </Box>
              ))
            )}
          </Box>
        )}
      </Paper>
    </Container>
  );
}

export default Analizador;
