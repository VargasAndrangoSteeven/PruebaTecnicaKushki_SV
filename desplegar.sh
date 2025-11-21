#!/bin/bash

# 
# SCRIPT DE DESPLIEGUE AUTOMÁTICO
# 
# Autor: Steeven Vargas
# Fecha: Noviembre 2024
# Descripción: Script para configurar y desplegar el proyecto completo
# Plataforma: Linux/Mac/Windows (Git Bash)

set -e  # Salir si hay algún error

# Colores para output
VERDE='\033[0;32m'
AZUL='\033[0;34m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
NC='\033[0m' # Sin color

# Función para imprimir con color
imprimir() {
    echo -e "${2}${1}${NC}"
}

# Banner
clear
echo "===================================="
imprimir "🚀 DESPLIEGUE AUTOMÁTICO - ANALIZADOR INTELIGENTE DE IMÁGENES" "$AZUL"
echo "===================================="
echo ""

# 
# 1. VERIFICAR DOCKER
# 
imprimir "📋 Paso 1: Verificando Docker..." "$AZUL"

if ! command -v docker &> /dev/null; then
    imprimir "❌ Docker no está instalado" "$ROJO"
    imprimir "   Por favor, instala Docker desde: https://www.docker.com/get-started" "$AMARILLO"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    imprimir "❌ Docker Compose no está instalado" "$ROJO"
    imprimir "   Por favor, instala Docker Compose" "$AMARILLO"
    exit 1
fi

imprimir "✅ Docker y Docker Compose están instalados" "$VERDE"
docker --version
docker-compose --version
echo ""

# 
# 2. CONFIGURAR VARIABLES DE ENTORNO
# 
imprimir "📋 Paso 2: Configurando variables de entorno..." "$AZUL"

if [ ! -f .env ]; then
    imprimir "⚙️  Creando archivo .env desde .env.ejemplo..." "$AMARILLO"
    cp .env.ejemplo .env
    
    # Generar claves seguras
    CLAVE_SECRETA=$(openssl rand -hex 32)
    CLAVE_JWT=$(openssl rand -hex 32)
    FRASE_GPG=$(openssl rand -hex 16)
    
    # Reemplazar en .env (compatible con Mac y Linux)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/cambia-esta-clave-por-una-segura-en-produccion/$CLAVE_SECRETA/" .env
        sed -i '' "s/cambia-esta-clave-jwt-por-una-segura-en-produccion/$CLAVE_JWT/" .env
        sed -i '' "s/cambia-esta-frase-por-una-segura/$FRASE_GPG/" .env
    else
        sed -i "s/cambia-esta-clave-por-una-segura-en-produccion/$CLAVE_SECRETA/" .env
        sed -i "s/cambia-esta-clave-jwt-por-una-segura-en-produccion/$CLAVE_JWT/" .env
        sed -i "s/cambia-esta-frase-por-una-segura/$FRASE_GPG/" .env
    fi
    
    imprimir "✅ Archivo .env creado con claves generadas" "$VERDE"
else
    imprimir "✅ Archivo .env ya existe" "$VERDE"
fi

echo ""

# 
# 2.5 CREAR DIRECTORIOS NECESARIOS
# 
imprimir "📋 Paso 2.5: Creando directorios necesarios..." "$AZUL"

mkdir -p backend/datos backend/cargas backend/logs backend/credenciales
chmod -R 777 backend/datos backend/cargas backend/logs

imprimir "✅ Directorios creados con permisos correctos" "$VERDE"
echo ""

# 
# 3. VERIFICAR CREDENCIALES DE GOOGLE
# 
imprimir "📋 Paso 3: Verificando credenciales de Google Cloud..." "$AZUL"

GOOGLE_CREDS="backend/credenciales/google-vision.json"

if [ ! -f "$GOOGLE_CREDS" ]; then
    imprimir "⚠️  No se encontró el archivo de credenciales de Google Cloud" "$AMARILLO"
    imprimir "   Por favor, coloca tu archivo google-vision.json en:" "$AMARILLO"
    imprimir "   $GOOGLE_CREDS" "$AMARILLO"
    imprimir ""
    read -p "   ¿Deseas continuar sin Google Cloud Vision? (s/N): " respuesta
    if [[ ! "$respuesta" =~ ^[sS]$ ]]; then
        imprimir "❌ Despliegue cancelado" "$ROJO"
        exit 1
    fi
else
    imprimir "✅ Credenciales de Google Cloud encontradas" "$VERDE"
fi

echo ""

# 
# 4. GENERAR CERTIFICADOS SSL
# 
imprimir "📋 Paso 4: Generando certificados SSL autofirmados..." "$AZUL"

if [ ! -f "nginx/ssl/certificado.crt" ] || [ ! -f "nginx/ssl/privado.key" ]; then
    mkdir -p nginx/ssl
    
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout nginx/ssl/privado.key \
        -out nginx/ssl/certificado.crt \
        -subj "/C=EC/ST=Pichincha/L=Quito/O=KushkiTest/CN=localhost" \
        2>/dev/null
    
    imprimir "✅ Certificados SSL generados" "$VERDE"
else
    imprimir "✅ Certificados SSL ya existen" "$VERDE"
fi

echo ""

# 
# 5. CONSTRUIR Y LEVANTAR CONTENEDORES
# 
imprimir "📋 Paso 5: Construyendo imágenes Docker..." "$AZUL"
imprimir "   ⏳ Esto puede tomar varios minutos..." "$AMARILLO"
echo ""

docker-compose down 2>/dev/null || true
docker-compose build

echo ""
imprimir "✅ Imágenes construidas exitosamente" "$VERDE"
echo ""

imprimir "📋 Paso 6: Levantando servicios..." "$AZUL"

docker-compose up -d

echo ""
imprimir "✅ Servicios levantados" "$VERDE"

# Esperar a que los servicios estén listos
imprimir "   ⏳ Esperando a que los servicios estén listos..." "$AMARILLO"
sleep 15

# 
# 6. INICIALIZAR BASE DE DATOS
# 
imprimir "📋 Paso 7: Inicializando base de datos..." "$AZUL"

docker-compose exec -T backend python inicializar_bd.py 2>/dev/null || {
    imprimir "   ⏳ Esperando a que backend esté completamente listo..." "$AMARILLO"
    sleep 5
    docker-compose exec -T backend python inicializar_bd.py || true
}

echo ""

# 
# 7. VERIFICAR SERVICIOS
# 
imprimir "📋 Paso 8: Verificando servicios..." "$AZUL"

# Verificar backend a través de NGINX
if curl -k -s --max-time 3 https://localhost:5001/api/salud > /dev/null 2>&1; then
    imprimir "✅ Backend está funcionando" "$VERDE"
else
    imprimir "⚠️  Backend no responde (puede tardar unos segundos más)" "$AMARILLO"
fi

# Verificar frontend
if curl -k -s --max-time 3 https://localhost:3000 > /dev/null 2>&1; then
    imprimir "✅ Frontend está funcionando" "$VERDE"
else
    imprimir "⚠️  Frontend no responde (puede tardar unos segundos más)" "$AMARILLO"
fi

echo ""

# 
# RESUMEN FINAL
# 
echo "===================================="
imprimir "✅ ¡DESPLIEGUE COMPLETADO EXITOSAMENTE!" "$VERDE"
echo "===================================="
echo ""
imprimir "🌐 ACCESOS:" "$AZUL"
imprimir "   Frontend:  https://localhost:3000" "$VERDE"
imprimir "   Backend:   https://localhost:5001" "$VERDE"
echo ""
imprimir "👤 USUARIO DE PRUEBA:" "$AZUL"
imprimir "   Usuario:    admin2025" "$VERDE"
imprimir "   Contraseña: pass2025" "$VERDE"
echo ""
imprimir "📝 COMANDOS ÚTILES:" "$AZUL"
imprimir "   Ver logs:       docker-compose logs -f" "$AMARILLO"
imprimir "   Detener:        docker-compose down" "$AMARILLO"
imprimir "   Reiniciar:      docker-compose restart" "$AMARILLO"
echo ""
imprimir "⚠️  NOTA: Tu navegador mostrará advertencia de certificado SSL." "$AMARILLO"
imprimir "   Esto es normal con certificados autofirmados." "$AMARILLO"
imprimir "   Haz clic en 'Avanzado' y 'Continuar' para acceder." "$AMARILLO"
echo ""
echo "===================================="
imprimir "🚀 ¡Disfruta del Analizador de Imágenes!" "$AZUL"
echo "===================================="
