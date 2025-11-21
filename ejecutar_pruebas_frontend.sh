#!/bin/bash

# 
# SCRIPT PARA EJECUTAR PRUEBAS DEL FRONTEND
# 
# Autor: Steeven Vargas
# Fecha: Noviembre 2024
# Descripción: Ejecuta pruebas automatizadas del frontend con Jest

echo ""
echo "EJECUTANDO PRUEBAS DEL FRONTEND (JEST)"
echo ""
echo ""

# Verificar que Node.js esté instalado localmente
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js no está instalado en tu sistema"
    echo ""
    echo "Las pruebas del frontend requieren Node.js localmente."
    echo "El contenedor de producción (Nginx) no tiene Node.js."
    echo ""
    echo "Opciones:"
    echo "  1) Instalar Node.js: https://nodejs.org/"
    echo "  2) Usar Docker con una imagen temporal de Node"
    echo ""
    read -p "¿Deseas ejecutar con Docker temporal? [s/N]: " USE_DOCKER

    if [[ $USE_DOCKER =~ ^[Ss]$ ]]; then
        USE_DOCKER_MODE=true
    else
        echo "❌ Cancelado. Instala Node.js para ejecutar pruebas."
        exit 1
    fi
else
    echo "✓ Node.js encontrado: $(node --version)"
    USE_DOCKER_MODE=false
fi

echo ""
echo "ℹ️  NOTA: El frontend actual no tiene archivos de prueba (.test.js)"
echo "   Pero el entorno de pruebas está configurado en package.json"
echo ""

# Opción 1: Ejecutar todas las pruebas
echo "📋 Opciones de ejecución:"
echo "  1) Ejecutar pruebas (si existen archivos .test.js)"
echo "  2) Ejecutar pruebas con COBERTURA"
echo "  3) Ejecutar pruebas en modo WATCH"
echo "  4) Crear archivo de prueba de EJEMPLO"
echo ""

if [ "$1" != "" ]; then
    OPCION=$1
else
    read -p "Selecciona una opción [1-4]: " OPCION
fi

case $OPCION in
    1)
        echo ""
        echo "🧪 Ejecutando todas las pruebas del frontend..."
        echo ""
        if [ "$USE_DOCKER_MODE" = true ]; then
            docker run --rm -v "$(pwd)/frontend:/app" -w /app node:18-alpine sh -c "npm install --silent && CI=true npm test -- --watchAll=false"
        else
            cd frontend && CI=true npm test -- --watchAll=false
        fi
        ;;
    2)
        echo ""
        echo "🧪 Ejecutando pruebas con cobertura de código..."
        echo ""
        if [ "$USE_DOCKER_MODE" = true ]; then
            docker run --rm -v "$(pwd)/frontend:/app" -w /app node:18-alpine sh -c "npm install --silent && CI=true npm test -- --coverage --watchAll=false"
        else
            cd frontend && CI=true npm test -- --coverage --watchAll=false
        fi
        ;;
    3)
        echo ""
        if [ "$USE_DOCKER_MODE" = true ]; then
            echo "⚠️  NOTA: El modo watch no funciona en Docker temporal"
            echo "   Ejecutando pruebas una sola vez..."
            echo ""
            docker run --rm -v "$(pwd)/frontend:/app" -w /app node:18-alpine sh -c "npm install --silent && CI=true npm test -- --watchAll=false"
        else
            echo "🧪 Ejecutando pruebas en modo watch (se ejecutan al guardar)..."
            echo "   Presiona 'q' para salir"
            echo ""
            cd frontend && npm test
        fi
        ;;
    4)
        echo ""
        echo "📝 Creando archivo de prueba de ejemplo..."
        cat > frontend/src/App.test.js << 'EOF'
/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Pruebas de ejemplo para React
 */

import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  test('renderiza la aplicación sin errores', () => {
    render(<App />);
    // Esta prueba simplemente verifica que la app se renderice
    expect(true).toBe(true);
  });
});
EOF
        echo "✓ Archivo creado: frontend/src/App.test.js"
        echo ""
        echo "Ahora puedes ejecutar las pruebas con la opción 1"
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo ""
echo "✓ Ejecución completada"
echo ""
