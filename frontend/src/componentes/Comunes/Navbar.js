/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Barra de navegación
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box
} from '@mui/material';
import { Logout, Image, History } from '@mui/icons-material';

function Navbar({ alCerrarSesion }) {
  const navigate = useNavigate();

  const manejarCerrarSesion = () => {
    alCerrarSesion();
    navigate('/login');
  };

  return (
    <AppBar
      position="static"
      sx={{
        background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)'
      }}
    >
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
          Analizador de Imágenes
        </Typography>
        
        <Box>
          <Button
            color="inherit"
            startIcon={<Image />}
            onClick={() => navigate('/analizador')}
            sx={{
              borderRadius: 2,
              mx: 0.5,
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.1)'
              }
            }}
          >
            Analizador
          </Button>

          <Button
            color="inherit"
            startIcon={<History />}
            onClick={() => navigate('/historial')}
            sx={{
              borderRadius: 2,
              mx: 0.5,
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.1)'
              }
            }}
          >
            Historial
          </Button>

          <Button
            color="inherit"
            startIcon={<Logout />}
            onClick={manejarCerrarSesion}
            sx={{
              borderRadius: 2,
              mx: 0.5,
              '&:hover': {
                background: 'rgba(255, 255, 255, 0.1)'
              }
            }}
          >
            Cerrar Sesión
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
