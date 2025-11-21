#!/bin/bash

# 
# SCRIPT PARA EJECUTAR PRUEBAS DEL BACKEND
# 
# Autor: Steeven Vargas
# Fecha: Noviembre 2024
# Descripción: Ejecuta pruebas automatizadas del backend con pytest

echo ""
echo "EJECUTANDO PRUEBAS DEL BACKEND (PYTEST)"
echo ""
echo ""

# Verificar que el contenedor esté corriendo
if ! docker ps | grep -q "analizador-backend"; then
    echo "❌ Error: El contenedor del backend no está corriendo"
    echo "   Ejecuta primero: docker-compose up -d backend"
    exit 1
fi

echo "✓ Contenedor backend encontrado"
echo ""

# Opción 1: Ejecutar todas las pruebas
echo "📋 Opciones de ejecución:"
echo "  1) Ejecutar TODAS las pruebas"
echo "  2) Ejecutar pruebas con REPORTE DETALLADO"
echo "  3) Ejecutar pruebas con COBERTURA"
echo "  4) Ejecutar pruebas ESPECÍFICAS (por clase)"
echo "  5) Ejecutar prueba INDIVIDUAL"
echo ""

# Si se pasa argumento, usar ese modo
if [ "$1" != "" ]; then
    OPCION=$1
else
    read -p "Selecciona una opción [1-5]: " OPCION
fi

case $OPCION in
    1)
        echo ""
        echo "🧪 Ejecutando todas las pruebas..."
        echo ""
        docker exec analizador-backend pytest /app/pruebas/ -v
        ;;
    2)
        echo ""
        echo "🧪 Ejecutando pruebas con reporte detallado..."
        echo ""
        docker exec analizador-backend pytest /app/pruebas/ -v --tb=short -s
        ;;
    3)
        echo ""
        echo "🧪 Ejecutando pruebas con cobertura de código..."
        echo ""
        docker exec analizador-backend pytest /app/pruebas/ -v --cov=/app --cov-report=term-missing
        ;;
    4)
        echo ""
        echo "Clases de prueba disponibles:"
        echo "  - TestRegistro"
        echo "  - TestInicioSesion"
        echo "  - TestVerificacionToken"
        echo ""
        read -p "Ingresa el nombre de la clase (ej: TestRegistro): " CLASE
        echo ""
        echo "🧪 Ejecutando pruebas de la clase $CLASE..."
        echo ""
        docker exec analizador-backend pytest /app/pruebas/test_autenticacion.py::$CLASE -v
        ;;
    5)
        echo ""
        echo "Ejemplo: TestRegistro::test_registro_exitoso"
        echo ""
        read -p "Ingresa Clase::nombre_test: " TEST
        echo ""
        echo "🧪 Ejecutando prueba específica: $TEST..."
        echo ""
        docker exec analizador-backend pytest /app/pruebas/test_autenticacion.py::$TEST -v -s
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

echo ""
echo ""
echo "✓ Ejecución de pruebas completada"
echo ""
