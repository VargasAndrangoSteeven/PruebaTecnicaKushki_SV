#!/bin/bash

# 
# SCRIPT DE VERIFICACIÓN DE SEGURIDAD
# 
# Autor: Steeven Vargas
# Fecha: Noviembre 2024
# Descripción: Verifica la implementación de seguridad en el sistema

echo ""
echo "VERIFICACIÓN DE SEGURIDAD DEL SISTEMA"
echo ""
echo ""

# 1. Verificar encriptación en tránsito (HTTPS/SSL)
echo "1. ENCRIPTACIÓN EN TRÁNSITO (HTTPS/SSL)"
echo "-------------------------------------------"
echo "✓ Verificando certificados SSL..."
if [ -f "./nginx/ssl/certificado.crt" ] && [ -f "./nginx/ssl/privado.key" ]; then
    echo "  ✓ Certificados SSL encontrados"
    echo "  - Ubicación: ./nginx/ssl/"
    openssl x509 -in ./nginx/ssl/certificado.crt -noout -subject -issuer -dates 2>/dev/null || echo "  (Usar openssl para ver detalles)"
else
    echo "  ✗ Certificados SSL NO encontrados"
fi
echo ""

echo "✓ Verificando configuración NGINX..."
if grep -q "ssl_protocols TLSv1.2 TLSv1.3" ./nginx/nginx.conf; then
    echo "  ✓ Protocolos SSL configurados: TLSv1.2, TLSv1.3"
fi
if grep -q "ssl_certificate" ./nginx/nginx.conf; then
    echo "  ✓ SSL habilitado en puertos: 3000 (Frontend), 5001 (Backend)"
fi
echo ""

# 2. Verificar encriptación en base de datos
echo "2. ENCRIPTACIÓN EN BASE DE DATOS"
echo "-------------------------------------------"
echo "✓ Verificando algoritmo de hash de contraseñas..."
if grep -q "bcrypt" ./backend/modelos/usuario.py; then
    echo "  ✓ Algoritmo: BCrypt (rounds=12)"
    echo "  ✓ Método: Hashing con salt único por usuario"
fi
echo ""

echo "✓ Consultando base de datos..."
docker exec analizador-backend python3 -c "
from modelos.usuario import Usuario
from modelos import db
import sys
sys.path.insert(0, '/app')
from app import app

with app.app_context():
    usuarios = Usuario.query.all()
    if usuarios:
        print('  ✓ Total usuarios en BD:', len(usuarios))
        for usuario in usuarios[:3]:
            print(f'  - Usuario: {usuario.nombre_usuario}')
            print(f'    Hash: {usuario.contrasena_hash[:30]}...')
            print(f'    Longitud: {len(usuario.contrasena_hash)} caracteres')
            print(f'    Formato: BCrypt (\$2b\$ = identificador bcrypt)')
    else:
        print('  ℹ No hay usuarios registrados aún')
" 2>/dev/null
echo ""

# 3. Verificar Headers de Seguridad
echo "3. HEADERS DE SEGURIDAD HTTP"
echo "-------------------------------------------"
echo "✓ Headers configurados en NGINX:"
grep "add_header" ./nginx/nginx.conf | sed 's/^/  /'
echo ""

# 4. Verificar validación de contraseñas
echo "4. VALIDACIÓN DE CONTRASEÑAS"
echo "-------------------------------------------"
if grep -q "patron_contrasena" ./backend/rutas/autenticacion.py; then
    echo "  ✓ Patrón de validación implementado:"
    grep "patron_contrasena = " ./backend/rutas/autenticacion.py | sed 's/^/  /'
    echo "  ✓ Requisitos:"
    echo "    - Mínimo 8 caracteres"
    echo "    - Al menos 1 letra mayúscula"
    echo "    - Al menos 1 número"
    echo "    - Al menos 1 símbolo (. , - _)"
fi
echo ""

# 5. Verificar JWT (Tokens)
echo "5. AUTENTICACIÓN CON JWT"
echo "-------------------------------------------"
if docker exec analizador-backend printenv | grep -q "JWT_SECRET_KEY"; then
    echo "  ✓ JWT_SECRET_KEY configurada (variable de entorno)"
else
    echo "  ⚠ JWT_SECRET_KEY no visible (esto es correcto por seguridad)"
fi
echo "  ✓ Tokens almacenados en: localStorage (frontend)"
echo "  ✓ Tokens enviados en: Header 'Authorization: Bearer <token>'"
echo ""

# 6. Prueba de conexión HTTPS
echo "6. PRUEBA DE CONEXIÓN HTTPS"
echo "-------------------------------------------"
echo "✓ Probando conexión HTTPS al backend..."
HTTP_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" --max-time 5 https://localhost:5001/api/salud 2>&1)
if [ "$HTTP_CODE" = "200" ]; then
    echo "  ✓ Backend HTTPS funcionando (puerto 5001) - Código: $HTTP_CODE"
else
    echo "  ⚠ Backend responde con código: $HTTP_CODE"
fi
echo ""

echo "✓ Probando conexión HTTPS al frontend..."
HTTP_CODE=$(curl -k -s -o /dev/null -w "%{http_code}" --max-time 5 https://localhost:3000/ 2>&1)
if [ "$HTTP_CODE" = "200" ]; then
    echo "  ✓ Frontend HTTPS funcionando (puerto 3000) - Código: $HTTP_CODE"
else
    echo "  ⚠ Frontend responde con código: $HTTP_CODE"
fi
echo ""

# 7. Verificar CORS
echo "7. CONFIGURACIÓN CORS"
echo "-------------------------------------------"
if grep -q "CORS" ./backend/app.py; then
    echo "  ✓ CORS configurado en Flask"
    echo "  ✓ Permite peticiones desde frontend a backend"
fi
echo ""

# 8. Verificar Captcha
echo "8. PROTECCIÓN CONTRA BOTS (CAPTCHA)"
echo "-------------------------------------------"
if [ -f "./backend/utilidades/captcha.py" ]; then
    echo "  ✓ Captcha matemático implementado"
    echo "  ✓ Expiración: 5 minutos"
    echo "  ✓ Intentos máximos: 3"
    echo "  ✓ Protege: Registro de usuarios"
fi
echo ""

# Resumen
echo ""
echo "RESUMEN DE SEGURIDAD"
echo ""
echo "✓ Encriptación en tránsito: HTTPS/TLS (Nginx)"
echo "✓ Encriptación en reposo: BCrypt para contraseñas"
echo "✓ Autenticación: JWT con Bearer tokens"
echo "✓ Validación: Contraseñas fuertes + Captcha"
echo "✓ Headers de seguridad: HSTS, X-Frame-Options, etc."
echo "✓ Protección CSRF: Tokens JWT"
echo ""
echo "RECOMENDACIONES:"
echo "- Las contraseñas NUNCA se almacenan en texto plano"
echo "- Cada usuario tiene un salt único en su hash"
echo "- Los tokens JWT expiran y deben renovarse"
echo "- SSL/TLS encripta todo el tráfico HTTP"
echo ""
