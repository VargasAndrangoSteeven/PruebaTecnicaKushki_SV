/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Modal de bienvenida que se muestra en el primer inicio de sesión
 */

import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Avatar
} from '@mui/material';
import { Person, School, Work } from '@mui/icons-material';

function ModalBienvenida({ abierto, alCerrar }) {
  return (
    <Dialog
      open={abierto}
      onClose={alCerrar}
      maxWidth="sm"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 3,
          background: 'rgba(255, 255, 255, 0.98)',
          backdropFilter: 'blur(10px)'
        }
      }}
    >
      <DialogTitle sx={{ textAlign: 'center', pt: 4 }}>
        <Avatar
          sx={{
            width: 80,
            height: 80,
            margin: '0 auto 16px',
            background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
            fontSize: '2rem'
          }}
        >
          SV
        </Avatar>
        <Typography variant="h4" sx={{ fontWeight: 600, color: '#1a237e' }}>
          ¡Bienvenido!
        </Typography>
      </DialogTitle>

      <DialogContent>
        <Box sx={{ py: 2 }}>
          <Typography
            variant="h6"
            sx={{ mb: 3, textAlign: 'center', color: '#1976d2', fontWeight: 600 }}
          >
            Hola, mi nombre es Steeven Vargas
          </Typography>

          <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
            <Person sx={{ color: '#1976d2', fontSize: 28 }} />
            <Typography variant="body1">
              Tengo <strong>25 años</strong> y soy Ingeniero de Software
            </Typography>
          </Box>

          <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
            <School sx={{ color: '#1976d2', fontSize: 28 }} />
            <Typography variant="body1">
              Cuento con una <strong>Maestría en Gestión de Proyectos</strong>
            </Typography>
          </Box>

          <Box sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
            <Work sx={{ color: '#1976d2', fontSize: 28 }} />
            <Typography variant="body1">
              Me encanta crear <strong>soluciones innovadoras</strong> y aplicar toda mi curiosidad para aprender y gestionar recursos
            </Typography>
          </Box>

          <Box
            sx={{
              mt: 3,
              p: 2,
              background: 'linear-gradient(45deg, rgba(25, 118, 210, 0.1) 30%, rgba(66, 165, 245, 0.1) 90%)',
              borderRadius: 2,
              textAlign: 'center'
            }}
          >
            <Typography
              variant="h6"
              sx={{ color: '#1976d2', fontWeight: 600 }}
            >
              Muchas gracias por la oportunidad
            </Typography>
          </Box>
        </Box>
      </DialogContent>

      <DialogActions sx={{ justifyContent: 'center', pb: 3 }}>
        <Button
          onClick={alCerrar}
          variant="contained"
          size="large"
          sx={{
            px: 4,
            borderRadius: 2,
            background: 'linear-gradient(45deg, #1976d2 30%, #42a5f5 90%)',
            '&:hover': {
              background: 'linear-gradient(45deg, #1565c0 30%, #1976d2 90%)'
            }
          }}
        >
          ¡Comenzar!
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default ModalBienvenida;
