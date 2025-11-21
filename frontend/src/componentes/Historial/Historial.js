/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Componente de historial de análisis
 */

import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Card,
  CardContent,
  Grid,
  Chip,
  Alert,
  LinearProgress
} from '@mui/material';
import { Visibility, Close } from '@mui/icons-material';

function Historial() {
  const [historial, setHistorial] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [cargandoDetalles, setCargandoDetalles] = useState(false);
  const [dialogoAbierto, setDialogoAbierto] = useState(false);
  const [analisisSeleccionado, setAnalisisSeleccionado] = useState(null);
  const [imagenUrl, setImagenUrl] = useState('');

  useEffect(() => {
    cargarHistorial();
  }, []);

  const cargarHistorial = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${process.env.REACT_APP_API_URL}/api/historial`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();
      if (data.exito) {
        setHistorial(data.datos.analisis);
      }
    } catch (error) {
      console.error('Error al cargar historial:', error);
    } finally {
      setCargando(false);
    }
  };

  const abrirDetalles = async (analisis) => {
    setCargandoDetalles(true);
    try {
      const token = localStorage.getItem('token');

      const responseDetalles = await fetch(
        `${process.env.REACT_APP_API_URL}/api/historial/${analisis.id}`,
        {
          headers: { 'Authorization': `Bearer ${token}` }
        }
      );
      const dataDetalles = await responseDetalles.json();

      if (dataDetalles.exito) {
        setAnalisisSeleccionado(dataDetalles.datos);

        const responseImagen = await fetch(
          `${process.env.REACT_APP_API_URL}/api/historial/${analisis.id}/imagen`,
          {
            headers: { 'Authorization': `Bearer ${token}` }
          }
        );

        if (responseImagen.ok) {
          const blob = await responseImagen.blob();
          const url = URL.createObjectURL(blob);
          setImagenUrl(url);
        }

        setDialogoAbierto(true);
      }
    } catch (error) {
      console.error('Error al cargar detalles:', error);
    } finally {
      setCargandoDetalles(false);
    }
  };

  const cerrarDialogo = () => {
    setDialogoAbierto(false);
    if (imagenUrl) {
      URL.revokeObjectURL(imagenUrl);
      setImagenUrl('');
    }
    setAnalisisSeleccionado(null);
  };

  if (cargando) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
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
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600, color: '#1a237e' }}>
          Historial de Análisis
        </Typography>

        {historial.length === 0 ? (
          <Typography>No hay análisis previos</Typography>
        ) : (
          <Grid container spacing={3}>
            {historial.map((analisis) => (
              <Grid item xs={12} sm={6} md={4} key={analisis.id}>
                <Card elevation={2}>
                  <CardContent>
                    <Typography variant="h6" noWrap sx={{ mb: 1 }}>
                      {analisis.nombre_archivo}
                    </Typography>
                    <Chip
                      label={analisis.proveedor_ia === 'google' ? 'Google Vision' : 'Imagga'}
                      color="primary"
                      size="small"
                      sx={{ mb: 1 }}
                    />
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                      {new Date(analisis.fecha_analisis).toLocaleDateString('es-ES')}
                    </Typography>
                    <Button
                      variant="contained"
                      fullWidth
                      startIcon={<Visibility />}
                      onClick={() => abrirDetalles(analisis)}
                      sx={{
                        borderRadius: 2,
                        background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
                        '&:hover': {
                          background: 'linear-gradient(45deg, #1565c0 30%, #1976d2 90%)'
                        }
                      }}
                    >
                      Ver Detalles
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        )}
      </Paper>

      {/* Overlay de carga */}
      {cargandoDetalles && (
        <Box
          sx={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            zIndex: 9999,
            backdropFilter: 'blur(4px)'
          }}
        >
          <CircularProgress size={60} sx={{ color: '#42a5f5', mb: 2 }} />
          <Typography variant="h6" sx={{ color: 'white', fontWeight: 500 }}>
            Cargando información...
          </Typography>
          <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)', mt: 1 }}>
            Por favor espera un momento
          </Typography>
        </Box>
      )}

      {/* Diálogo de detalles */}
      <Dialog
        open={dialogoAbierto}
        onClose={cerrarDialogo}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Detalles del Análisis
          <Button
            onClick={cerrarDialogo}
            sx={{
              position: 'absolute',
              right: 8,
              top: 8,
              minWidth: 'auto',
              borderRadius: 2,
              color: '#1976d2',
              '&:hover': {
                background: 'rgba(25, 118, 210, 0.08)'
              }
            }}
          >
            <Close />
          </Button>
        </DialogTitle>
        <DialogContent dividers>
          {analisisSeleccionado && (
            <Box>
              {/* Imagen */}
              {imagenUrl && (
                <Box sx={{ mb: 3, textAlign: 'center' }}>
                  <img
                    src={imagenUrl}
                    alt={analisisSeleccionado.nombre_archivo}
                    style={{
                      maxWidth: '100%',
                      maxHeight: '400px',
                      borderRadius: '8px',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
                    }}
                  />
                </Box>
              )}

              {/* Información general */}
              <Typography variant="h6" gutterBottom>
                {analisisSeleccionado.nombre_archivo}
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Chip
                  label={analisisSeleccionado.proveedor_ia === 'google' ? 'Google Cloud Vision' : 'Imagga'}
                  color="primary"
                  sx={{ mr: 1 }}
                />
                <Typography variant="body2" color="text.secondary" component="span">
                  {new Date(analisisSeleccionado.fecha_analisis).toLocaleDateString('es-ES')}
                </Typography>
              </Box>

              {/* Interpretación */}
              {analisisSeleccionado.interpretacion && (
                <Alert severity="info" sx={{ mb: 3 }}>
                  <Typography variant="body1" sx={{ fontWeight: 'medium' }}>
                    {analisisSeleccionado.interpretacion}
                  </Typography>
                </Alert>
              )}

              {/* Etiquetas traducidas */}
              <Typography variant="subtitle1" gutterBottom sx={{ fontWeight: 'bold', mt: 2 }}>
                Etiquetas Detectadas:
              </Typography>

              {analisisSeleccionado.etiquetas_traducidas && analisisSeleccionado.etiquetas_traducidas.length > 0 ? (
                analisisSeleccionado.etiquetas_traducidas.map((etiqueta, index) => (
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
                analisisSeleccionado.etiquetas.map((etiqueta, index) => (
                  <Box key={index} sx={{ mb: 2.5 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 0.5 }}>
                      <Typography>{etiqueta.etiqueta}</Typography>
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
        </DialogContent>
        <DialogActions>
          <Button
            onClick={cerrarDialogo}
            variant="contained"
            sx={{
              borderRadius: 2,
              background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
              '&:hover': {
                background: 'linear-gradient(45deg, #1565c0 30%, #1976d2 90%)'
              }
            }}
          >
            Cerrar
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default Historial;
