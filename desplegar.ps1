# 
# SCRIPT DE DESPLIEGUE AUTOMÁTICO - WINDOWS
# 
# Autor: Steeven Vargas
# Fecha: Noviembre 2024
# Descripción: Script PowerShell para desplegar en Windows
# Plataforma: Windows PowerShell

$ErrorActionPreference = "Stop"

# Función para imprimir con color
function Imprimir {
    param([string]$Mensaje, [string]$Color = "White")
    Write-Host $Mensaje -ForegroundColor $Color
}

# Banner
Clear-Host
Write-Host "====================================" -ForegroundColor Blue
Imprimir "🚀 DESPLIEGUE AUTOMÁTICO - ANALIZADOR INTELIGENTE DE IMÁGENES" "Blue"
Write-Host "====================================" -ForegroundColor Blue
Write-Host ""

# 
# 1. VERIFICAR DOCKER
# 
Imprimir "📋 Paso 1: Verificando Docker..." "Blue"

try {
    $dockerVersion = docker --version
    $dockerComposeVersion = docker-compose --version
    
    Imprimir "✅ Docker y Docker Compose están instalados" "Green"
    Write-Host $dockerVersion
    Write-Host $dockerComposeVersion
} catch {
    Imprimir "❌ Docker no está instalado o no está en el PATH" "Red"
    Imprimir "   Por favor, instala Docker Desktop desde: https://www.docker.com/products/docker-desktop" "Yellow"
    exit 1
}

Write-Host ""

# 
# 2. CONFIGURAR VARIABLES DE ENTORNO
# 
Imprimir "📋 Paso 2: Configurando variables de entorno..." "Blue"

if (-Not (Test-Path ".env")) {
    Imprimir "⚙️  Creando archivo .env desde .env.ejemplo..." "Yellow"
    Copy-Item ".env.ejemplo" ".env"
    
    # Generar claves seguras (equivalente a openssl rand -hex)
    function Get-RandomHex {
        param([int]$Length)
        $bytes = New-Object byte[] ($Length)
        $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
        $rng.GetBytes($bytes)
        return [System.BitConverter]::ToString($bytes).Replace("-", "").ToLower()
    }
    
    $claveSecreta = Get-RandomHex 32
    $claveJWT = Get-RandomHex 32
    $fraseGPG = Get-RandomHex 16
    
    # Reemplazar en .env
    $content = Get-Content ".env"
    $content = $content -replace "cambia-esta-clave-por-una-segura-en-produccion", $claveSecreta
    $content = $content -replace "cambia-esta-clave-jwt-por-una-segura-en-produccion", $claveJWT
    $content = $content -replace "cambia-esta-frase-por-una-segura", $fraseGPG
    $content | Set-Content ".env"
    
    Imprimir "✅ Archivo .env creado con claves generadas" "Green"
    Imprimir "   🔑 Clave secreta: $($claveSecreta.Substring(0,8))********" "Green"
    Imprimir "   🔑 Clave JWT: $($claveJWT.Substring(0,8))********" "Green"
} else {
    Imprimir "✅ Archivo .env ya existe" "Green"
}

Write-Host ""
# 
# 2.5 CREAR DIRECTORIOS NECESARIOS
# 
Imprimir "📋 Paso 2.5: Creando directorios necesarios..." "Blue"

New-Item -ItemType Directory -Force -Path "backend\datos" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\cargas" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "backend\credenciales" | Out-Null

Imprimir "✅ Directorios creados" "Green"
Write-Host ""
# 
# 3. VERIFICAR CREDENCIALES DE GOOGLE
# 
Imprimir "📋 Paso 3: Verificando credenciales de Google Cloud..." "Blue"

$googleCreds = "backend\credenciales\google-vision.json"

if (-Not (Test-Path $googleCreds)) {
    Imprimir "⚠️  No se encontró el archivo de credenciales de Google Cloud" "Yellow"
    Imprimir "   Por favor, coloca tu archivo google-vision.json en:" "Yellow"
    Imprimir "   $googleCreds" "Yellow"
    Write-Host ""
    $respuesta = Read-Host "   ¿Deseas continuar sin Google Cloud Vision? (s/N)"
    if ($respuesta -notmatch '^[sS]$') {
        Imprimir "❌ Despliegue cancelado" "Red"
        exit 1
    }
} else {
    Imprimir "✅ Credenciales de Google Cloud encontradas" "Green"
}

Write-Host ""

# 
# 4. GENERAR CERTIFICADOS SSL
# 
Imprimir "📋 Paso 4: Generando certificados SSL autofirmados..." "Blue"

if (-Not (Test-Path "nginx\ssl\certificado.crt") -or -Not (Test-Path "nginx\ssl\privado.key")) {
    New-Item -ItemType Directory -Force -Path "nginx\ssl" | Out-Null
    
    # Usar OpenSSL si está disponible, sino usar certificado auto-firmado de PowerShell
    try {
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 `
            -keyout nginx\ssl\privado.key `
            -out nginx\ssl\certificado.crt `
            -subj "/C=EC/ST=Pichincha/L=Quito/O=KushkiTest/CN=localhost" 2>$null
        
        Imprimir "✅ Certificados SSL generados" "Green"
    } catch {
        Imprimir "⚠️  OpenSSL no disponible. Los certificados se generarán en Docker." "Yellow"
    }
} else {
    Imprimir "✅ Certificados SSL ya existen" "Green"
}

Write-Host ""

# 
# 5. CONSTRUIR Y LEVANTAR CONTENEDORES
# 
Imprimir "📋 Paso 5: Construyendo imágenes Docker..." "Blue"
Imprimir "   ⏳ Esto puede tomar varios minutos..." "Yellow"
Write-Host ""

docker-compose down 2>$null
docker-compose build

Write-Host ""
Imprimir "✅ Imágenes construidas exitosamente" "Green"
Write-Host ""

Imprimir "📋 Paso 6: Levantando servicios..." "Blue"

docker-compose up -d

Write-Host ""
Imprimir "✅ Servicios levantados" "Green"

# Esperar a que los servicios estén listos
Imprimir "   ⏳ Esperando a que los servicios estén listos..." "Yellow"
Start-Sleep -Seconds 15

# 
# 6. INICIALIZAR BASE DE DATOS
# 
Imprimir "📋 Paso 7: Inicializando base de datos..." "Blue"

try {
    docker-compose exec -T backend python inicializar_bd.py 2>$null
} catch {
    Imprimir "   ⏳ Esperando a que backend esté completamente listo..." "Yellow"
    Start-Sleep -Seconds 5
    docker-compose exec -T backend python inicializar_bd.py 2>$null
}

Write-Host ""

# 
# 7. VERIFICAR SERVICIOS
# 
Imprimir "📋 Paso 8: Verificando servicios..." "Blue"

try {
    $null = Invoke-WebRequest -Uri "https://localhost:5001/api/salud" -SkipCertificateCheck -UseBasicParsing -TimeoutSec 3
    Imprimir "✅ Backend está funcionando" "Green"
} catch {
    Imprimir "⚠️  Backend no responde (puede tardar unos segundos más)" "Yellow"
}

try {
    $null = Invoke-WebRequest -Uri "https://localhost:3000" -SkipCertificateCheck -UseBasicParsing -TimeoutSec 3
    Imprimir "✅ Frontend está funcionando" "Green"
} catch {
    Imprimir "⚠️  Frontend no responde (puede tardar unos segundos más)" "Yellow"
}

Write-Host ""

# 
# RESUMEN FINAL
# 
Write-Host "====================================" -ForegroundColor Green
Imprimir "✅ ¡DESPLIEGUE COMPLETADO EXITOSAMENTE!" "Green"
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Imprimir "🌐 ACCESOS:" "Blue"
Imprimir "   Frontend:  https://localhost:3000" "Green"
Imprimir "   Backend:   https://localhost:5001" "Green"
Write-Host ""
Imprimir "👤 USUARIO DE PRUEBA:" "Blue"
Imprimir "   Usuario:    admin2025" "Green"
Imprimir "   Contraseña: pass2025" "Green"
Write-Host ""
Imprimir "📝 COMANDOS ÚTILES:" "Blue"
Imprimir "   Ver logs:       docker-compose logs -f" "Yellow"
Imprimir "   Detener:        docker-compose down" "Yellow"
Imprimir "   Reiniciar:      docker-compose restart" "Yellow"
Write-Host ""
Imprimir "⚠️  NOTA: Tu navegador mostrará advertencia de certificado SSL." "Yellow"
Imprimir "   Esto es normal con certificados autofirmados." "Yellow"
Imprimir "   Haz clic en 'Avanzado' y 'Continuar' para acceder." "Yellow"
Write-Host ""
Write-Host "====================================" -ForegroundColor Blue
Imprimir "🚀 ¡Disfruta del Analizador de Imágenes!" "Blue"
Write-Host "====================================" -ForegroundColor Blue
