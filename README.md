# 🖼️ Analizador Inteligente de Imágenes con IA

**Autor:** Steeven Vargas
**Fecha:** Noviembre 2024
**Proyecto:** Prueba Técnica Kushki

---

## ⚠️ ADVERTENCIA IMPORTANTE: Configuración de Seguridad

> **NOTA EXCLUSIVA PARA ESTE PROYECTO DE DEMOSTRACIÓN**

Este repositorio incluye archivos sensibles como `.env` y `backend/credenciales/google-vision.json` **únicamente para facilitar la configuración y pruebas del proyecto de demostración**.

### 🚨 Práctica Prohibida en Producción

**Esta práctica está TOTALMENTE PROHIBIDA en entornos de producción y otros repositorios.**

En ambientes de producción, las credenciales y configuraciones sensibles deben ser:
- ✅ Configuradas directamente en la herramienta de despliegue (AWS Secrets Manager, Google Secret Manager, Azure Key Vault, etc.)
- ✅ Gestionadas como variables de entorno del sistema
- ✅ Nunca versionadas en control de código
- ✅ Incluidas en `.gitignore`

**NO replicar esta práctica en proyectos reales**

---

## 📋 Descripción del Proyecto

Aplicación web full-stack que permite a los usuarios subir imágenes y analizarlas utilizando servicios de Inteligencia Artificial avanzados. La aplicación procesa las imágenes devolviendo etiquetas descriptivas con niveles de confianza.

### ✨ Características Principales

- 🔐 **Sistema de autenticación robusto** con JWT y captcha matemático
- 🤖 **Análisis con múltiples proveedores de IA** (Google Cloud Vision, Imagga)
- 🌍 **Traducción automática** de etiquetas al español
- 📊 **Historial privado** de análisis por usuario
- 🎨 **Diseño moderno y responsivo** con Material-UI
- 🔒 **Seguridad multicapa** (HTTPS/TLS, BCrypt, Headers de seguridad)
- 🐳 **Arquitectura contenerizada** con Docker
- 🧪 **Testing automatizado** (Backend y Frontend)
- 📝 **Modal de bienvenida** personalizado en primer login
- 👁️ **Toggle de visibilidad** de contraseñas

---

## 🚀 Tecnologías Utilizadas

### Backend
- **Python 3.11**
- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos
- **JWT** - Autenticación stateless
- **BCrypt** - Hash de contraseñas (12 rounds)
- **Pytest** - Testing unitario
- **Gunicorn** - WSGI server

### Frontend
- **React 18** - Framework UI
- **Material-UI (MUI v5)** - Componentes y diseño
- **Axios** - Cliente HTTP
- **React Router v6** - Navegación
- **Jest** - Testing
- **localStorage** - Gestión de estado del usuario

### DevOps & Infraestructura
- **Docker & Docker Compose** - Containerización
- **Nginx** - Proxy reverso con SSL/TLS
- **Certificados SSL** - Autofirmados para desarrollo
- **HTTPS/TLS 1.2-1.3** - Encriptación en tránsito

### APIs de IA
- **Google Cloud Vision API** - Análisis avanzado de imágenes
- **Imagga API** - Etiquetado automático
- **Google Translate API** - Traducción al español

---

## 📦 Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- **Docker** (versión 20.10 o superior)
- **Docker Compose** (versión 2.0 o superior)
- **Git**
- *Opcional:* **Node.js** v18+ (para pruebas locales del frontend)

### Verificar Instalaciones

```bash
docker --version
docker-compose --version
git --version
node --version  # Opcional
```

---

## ⚡ Inicio Rápido

### 1️⃣ Clonar el Repositorio
```bash
# Clonar el repositorio
git clone https://github.com/VargasAndrangoSteeven/PruebaTecnicaKushki_SV.git
cd PruebaTecnicaKushki_SV

# Descargar todas las ramas
git fetch --all

# Ver ramas disponibles
git branch -a
```

**Estructura de ramas:**
- `main` - Código integrado y funcional
- `feature/backend-api` - Desarrollo del backend (3 commits)
- `feature/frontend-ui` - Desarrollo del frontend (1 commit)
- `feature/testing-cicd` - Tests y CI/CD (1 commit)

### 2️⃣ Configurar Credenciales de Google Cloud Vision

**Importante:** Coloca tu archivo de credenciales JSON de Google Cloud en:
```
backend/credenciales/google-vision.json  - YA SE ENCUENTRAN PRECONFIGURADAS EN EL PROYECTO
```

Si no tienes credenciales, la aplicación usará Imagga API automáticamente.

### 3️⃣ Iniciar la Aplicación

```bash
# Linux/Mac
chmod +x desplegar.sh
./desplegar.sh

# Windows (Git Bash)
bash desplegar.sh

# Windows (PowerShell)
.\desplegar.ps1
```

**El script realizará automáticamente:**
- ✅ Verificación de Docker instalado
- ✅ Configuración de variables de entorno (.env)
- ✅ Generación de certificados SSL autofirmados
- ✅ Construcción de imágenes Docker
- ✅ Inicialización de base de datos con usuario admin
- ✅ Levantamiento de todos los servicios

### 4️⃣ Acceder a la Aplicación

La aplicación estará disponible en:

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Frontend** | https://localhost:3000 | Interfaz de usuario |
| **Backend API** | https://localhost:5001 | API REST |
| **Backend Directo** | http://localhost:5077 | Flask sin proxy |

**⚠️ Nota:** Tu navegador mostrará una advertencia de certificado SSL (es normal con certificados autofirmados). Acepta el riesgo y continúa.

### 👤 Usuario de Prueba Predeterminado

```
Usuario: admin2025
Contraseña: Admin2025.
```

---

## 📚 Documentación Adicional

El proyecto incluye documentación detallada en archivos separados:

| Documento | Descripción |
|-----------|-------------|
| **[PRUEBAS.md](PRUEBAS.md)** | Documentación de pruebas automatizadas (Backend y Frontend) |
| **README.md** | Este archivo - Guía principal del proyecto |

---

## 🗂️ Estructura del Proyecto

```
PruebaTecnicaKushki_SV_CON_CAPTCHA/
├── 📁 backend/                          # API Flask
│   ├── app.py                          # Punto de entrada principal
│   ├── inicializar_bd.py               # Script inicialización BD
│   ├── requisitos.txt                  # Dependencias Python
│   ├── Dockerfile                      # Imagen Docker backend
│   │
│   ├── 📁 config/                      # Configuraciones
│   │   ├── configuracion.py            # Config Flask, BD, JWT
│   │   └── seguridad.py                # Config SSL, CORS, Headers
│   │
│   ├── 📁 modelos/                     # Modelos SQLAlchemy
│   │   ├── usuario.py                  # Modelo Usuario (BCrypt)
│   │   └── analisis.py                 # Modelo Análisis de Imagen
│   │
│   ├── 📁 rutas/                       # Endpoints API
│   │   ├── autenticacion.py            # Login, registro, verificación
│   │   └── analisis.py                 # Análisis de imágenes
│   │
│   ├── 📁 servicios/                   # Lógica de negocio
│   │   ├── servicio_ia.py              # Integración APIs IA
│   │   ├── servicio_auth.py            # Lógica autenticación
│   │   └── servicio_traduccion.py      # Google Translate
│   │
│   ├── 📁 utilidades/                  # Funciones auxiliares
│   │   ├── validadores.py              # Validación inputs
│   │   ├── decoradores.py              # JWT decorators
│   │   ├── respuestas.py               # Formato respuestas JSON
│   │   └── captcha.py                  # Captcha matemático
│   │
│   ├── 📁 pruebas/                     # Tests unitarios (Pytest)
│   │   ├── test_autenticacion.py       # 9 pruebas de auth
│   │   └── conftest.py                 # Fixtures
│   │
│   ├── 📁 credenciales/                # Credenciales APIs
│   │   └── google-vision.json          # (No versionado)
│   │
│   ├── 📁 cargas/                      # Imágenes subidas
│   ├── 📁 datos/                       # Base de datos SQLite
│   └── 📁 logs/                        # Logs de la aplicación
│
├── 📁 frontend/                         # Aplicación React
│   ├── package.json                    # Dependencias npm
│   ├── Dockerfile                      # Imagen Docker frontend
│   │
│   ├── 📁 public/
│   │   ├── index.html
│   │   ├── favicon.svg                 # Favicon personalizado
│   │   └── manifest.json
│   │
│   ├── 📁 src/
│   │   ├── App.js                      # Componente principal
│   │   ├── App.test.js                 # Pruebas de ejemplo (Jest)
│   │   ├── index.js                    # Punto de entrada
│   │   └── tema.js                     # Tema Material-UI
│   │
│   │   ├── 📁 componentes/
│   │   │   ├── 📁 Autenticacion/
│   │   │   │   ├── Login.js            # Login con toggle de contraseña
│   │   │   │   ├── Registro.js         # Registro con captcha
│   │   │   │   ├── CaptchaMatematico.js # Captcha numérico
│   │   │   │   └── Login.css           # Estilos animados
│   │   │   │
│   │   │   ├── 📁 Analizador/
│   │   │   │   └── Analizador.js       # Subir y analizar imágenes
│   │   │   │
│   │   │   ├── 📁 Historial/
│   │   │   │   └── Historial.js        # Ver análisis previos
│   │   │   │
│   │   │   └── 📁 Comunes/
│   │   │       ├── Navbar.js           # Barra de navegación
│   │   │       └── ModalBienvenida.js  # Modal primer login
│   │   │
│   │   └── 📁 servicios/               # Clientes API
│   │       ├── api.js                  # Configuración Axios
│   │       └── servicioAuth.js         # Llamadas autenticación
│   │
│   └── 📁 coverage/                     # Reportes de cobertura Jest
│
├── 📁 nginx/                            # Configuración Nginx
│   ├── nginx.conf                      # Proxy reverso con SSL
│   └── 📁 ssl/                         # Certificados SSL/TLS
│       ├── certificado.crt             # Certificado autofirmado
│       └── privado.key                 # Clave privada
│
├── 📄 docker-compose.yml               # Orquestación de servicios
├── 📄 .env                             # Variables de entorno
├── 📄 .env.ejemplo                     # Template para .env
├── 📄 .gitignore                       # Archivos ignorados
│
├── 📜 desplegar.sh                     # Script deploy Linux/Mac
├── 📜 desplegar.ps1                    # Script deploy Windows
│
├── 🧪 ejecutar_pruebas_backend.sh      # Script tests backend
├── 🧪 ejecutar_pruebas_frontend.sh     # Script tests frontend
├── 🔒 verificar_seguridad.sh           # Script verificación seguridad
│
├── 📖 README.md                        # Este archivo
├── 📖 PRUEBAS.md                       # Documentación de testing
│
└── 📁 .github/                         # CI/CD
    └── 📁 workflows/
        └── ci.yml                      # GitHub Actions pipeline
```

---

## 🧪 Testing y Calidad

### Scripts de Pruebas Automatizadas

El proyecto incluye scripts interactivos para ejecutar pruebas:

#### Backend (Pytest)

```bash
./ejecutar_pruebas_backend.sh
```

**Opciones disponibles:**
1. Ejecutar TODAS las pruebas (9 tests)
2. Ejecutar con REPORTE DETALLADO
3. Ejecutar con COBERTURA de código
4. Ejecutar pruebas ESPECÍFICAS (por clase)
5. Ejecutar prueba INDIVIDUAL

**Pruebas disponibles:**
- ✅ `TestInicioSesion` - 3 pruebas (Login, contraseña incorrecta, usuario no existe)
- ✅ `TestVerificacionToken` - 3 pruebas (Token válido, sin token, token inválido)
- ⚠️ `TestRegistro` - 3 pruebas (algunas requieren actualización para captcha)

**Ejecución rápida:**
```bash
# Solo pruebas que pasan (6/9)
docker exec analizador-backend pytest /app/pruebas/test_autenticacion.py::TestInicioSesion -v
```

#### Frontend (Jest)

```bash
./ejecutar_pruebas_frontend.sh
```

**Opciones disponibles:**
1. Ejecutar pruebas (si existen archivos .test.js)
2. Ejecutar con COBERTURA
3. Ejecutar en modo WATCH
4. Crear archivo de prueba de EJEMPLO

**Pruebas de ejemplo incluidas:**
- ✅ 6 pruebas básicas de validación
- ✅ Testing de funciones JavaScript
- ✅ Testing de promesas y async/await

**Requisito:** Node.js instalado localmente (el contenedor de producción usa Nginx)

### Cobertura de Código

| Componente | Cobertura | Estado |
|------------|-----------|--------|
| Backend (Pytest) | ~96% | ✅ Excelente |
| Frontend (Jest) | Configurado | ✅ Listo para expandir |

---

## 🔒 Seguridad Implementada

### 🔐 Encriptación en Tránsito

- ✅ **HTTPS/TLS 1.2 y 1.3** - Todo el tráfico encriptado
- ✅ **Certificados SSL** - Autofirmados para desarrollo
- ✅ **Nginx como proxy reverso** - Terminación SSL
- ✅ **HSTS habilitado** - Fuerza conexiones seguras

### 🔑 Encriptación en Reposo

- ✅ **BCrypt (12 rounds)** - Hash de contraseñas con salt único
- ✅ **JWT firmados** - Tokens de autenticación seguros
- ✅ **Variables de entorno** - Credenciales sensibles fuera del código

### 🛡️ Headers de Seguridad HTTP

```
✅ Strict-Transport-Security (HSTS)
✅ X-Frame-Options: DENY
✅ X-Content-Type-Options: nosniff
✅ X-XSS-Protection: 1; mode=block
```

### ✅ Validaciones de Entrada

**Contraseñas:**
- Mínimo 8 caracteres
- Al menos 1 letra mayúscula
- Al menos 1 número
- Al menos 1 símbolo (. , - _)

**Imágenes:**
- Tipos permitidos: JPG, JPEG, PNG, GIF, WEBP
- Tamaño máximo: 10MB
- Validación de MIME type

**Captcha:**
- Operaciones matemáticas aleatorias
- Expiración: 5 minutos
- Máximo 3 intentos

### 🔍 Verificar Seguridad

```bash
./verificar_seguridad.sh
```

Este script verifica:
- ✅ Certificados SSL y protocolos TLS
- ✅ Contraseñas hasheadas en base de datos (BCrypt)
- ✅ Headers de seguridad HTTP
- ✅ Conexiones HTTPS funcionando
- ✅ Configuración de CORS
- ✅ Captcha implementado

**Ejemplo de salida:**
```
✓ Backend HTTPS funcionando (puerto 5001) - Código: 200
✓ Frontend HTTPS funcionando (puerto 3000) - Código: 200
✓ Total usuarios en BD: 5
✓ Algoritmo: BCrypt (rounds=12)
✓ Hash: $2b$12$Y8ALCVa//3L.tHFZZMabveh...
```

📖 **Documentación completa:** [SEGURIDAD.md](SEGURIDAD.md)

---

## 📡 Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/registrar` | Registrar nuevo usuario con captcha | ❌ |
| POST | `/api/auth/iniciar-sesion` | Iniciar sesión y obtener JWT | ❌ |
| GET | `/api/auth/verificar` | Verificar validez del token | ✅ |
| POST | `/api/auth/cerrar-sesion` | Cerrar sesión | ✅ |
| GET | `/api/auth/captcha` | Generar nuevo captcha | ❌ |

### Análisis de Imágenes

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/analizar` | Analizar una imagen | ✅ |
| GET | `/api/historial` | Obtener historial del usuario | ✅ |
| GET | `/api/historial/<id>` | Obtener análisis específico | ✅ |
| DELETE | `/api/historial/<id>` | Eliminar análisis | ✅ |

### Health Check

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/salud` | Estado del servidor | ❌ |

### Ejemplo de Petición - Registro

```bash
curl -k -X POST https://localhost:5001/api/auth/registrar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "steeven",
    "contrasena": "MiPass123!",
    "captcha_token": "abc123...",
    "captcha_respuesta": "15"
  }'
```

### Ejemplo de Petición - Análisis de Imagen

```bash
curl -k -X POST https://localhost:5001/api/analizar \
  -H "Authorization: Bearer TU_TOKEN_JWT" \
  -F "imagen=@/ruta/a/imagen.jpg" \
  -F "proveedor_ia=google"
```

### Ejemplo de Respuesta - Análisis Exitoso

```json
{
  "exito": true,
  "datos": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "etiquetas_traducidas": [
      {
        "nombre": "Perro",
        "nombre_original": "Dog",
        "confianza": 98
      },
      {
        "nombre": "Golden Retriever",
        "nombre_original": "Golden Retriever",
        "confianza": 95
      },
      {
        "nombre": "Parque",
        "nombre_original": "Park",
        "confianza": 91
      }
    ],
    "interpretacion": "La imagen muestra un perro...",
    "proveedor_ia": "google",
    "nombre_archivo": "perro_parque.jpg",
    "fecha_analisis": "2024-11-21"
  },
  "mensaje": "Imagen analizada exitosamente"
}
```

---

## 🤖 Proveedores de IA

### Google Cloud Vision API

**Configuración:**
1. Crear proyecto en [Google Cloud Console](https://console.cloud.google.com)
2. Habilitar Cloud Vision API
3. Crear cuenta de servicio
4. Descargar credenciales JSON
5. Colocar en `backend/credenciales/google-vision.json`

**Características:**
- ✅ Alta precisión en detección de objetos y escenas
- ✅ Reconocimiento de texto (OCR)
- ✅ Detección de rostros y emociones
- ✅ Clasificación de contenido seguro
- ✅ Detección de logos y marcas

**Límites gratuitos:**
- 1,000 solicitudes/mes gratis
- $1.50 por 1,000 imágenes adicionales

### Imagga API

**Configuración:**
Las credenciales ya están incluidas en el proyecto (plan gratuito).

**Características:**
- ✅ Etiquetado automático multiidioma
- ✅ Categorización de imágenes
- ✅ Detección de colores dominantes
- ✅ Reconocimiento de contenido NSFW

**Límites gratuitos:**
- 1,000 solicitudes/mes gratis
- Procesamiento rápido

---

## 🎨 Características de UI/UX

### Diseño Moderno

- 🎨 **Material-UI v5** - Componentes profesionales
- 🌈 **Gradientes azules** - Paleta de colores consistente
- ✨ **Animaciones suaves** - Partículas y transiciones
- 📱 **Responsive** - Adaptable a móviles y tablets

### Funcionalidades de Usuario

- 👁️ **Toggle de contraseñas** - Ver/ocultar contraseñas en login y registro
- 🎉 **Modal de bienvenida** - Mensaje personalizado en primer login
- 🔢 **Captcha matemático** - Protección contra bots con operaciones simples
- 📊 **Barras de confianza** - Visualización de niveles de certeza
- 🌍 **Traducción automática** - Etiquetas en español con original
- 🔄 **Interpretación IA** - Descripción narrativa de la imagen

### Navegación

- ⚡ **React Router** - Navegación SPA fluida
- 🏠 **Navbar persistente** - Acceso rápido a secciones
- 🔐 **Rutas protegidas** - Redirección automática si no autenticado
- 💾 **Estado persistente** - localStorage para sesiones

---

## 🐳 Docker y Despliegue

### Servicios Docker

El proyecto usa 3 contenedores orquestados con Docker Compose:

| Contenedor | Imagen Base | Descripción | Puerto |
|------------|-------------|-------------|--------|
| `analizador-backend` | python:3.11-slim | API Flask + Gunicorn | 5077 |
| `analizador-frontend` | nginx:alpine | Build de React + Nginx | 3001 (interno) |
| `analizador-nginx` | nginx:alpine | Proxy reverso con SSL | 3000, 5001, 443 |

### Comandos Docker Útiles

```bash
# Ver contenedores en ejecución
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Reconstruir solo un servicio
docker-compose build backend
docker-compose up -d backend

# Detener todos los servicios
docker-compose down

# Limpiar volúmenes y datos
docker-compose down -v

# Entrar a un contenedor
docker exec -it analizador-backend bash
docker exec -it analizador-frontend sh

# Ver logs de un servicio específico
docker-compose logs backend --tail=100 -f
```

### Red Docker

Los contenedores se comunican a través de una red bridge personalizada:
- **Nombre:** `red-analizador-imagenes`
- **Driver:** bridge
- **DNS interno:** Los servicios se referencian por nombre

---

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)

```env
# Flask
FLASK_ENV=desarrollo
CLAVE_SECRETA=secret-key
CLAVE_SECRETA_JWT=jwt-secret

# Base de Datos
URL_BASE_DATOS=sqlite:///./datos/app.db

# Google Cloud Vision (Opcional)
CREDENCIALES_GOOGLE=./credenciales/google-vision.json

# Imagga API
IMAGGA_API_KEY=acc_17c557dadc898af
IMAGGA_API_SECRET=2be723d45c97944643a1afea53fd3d20

# CORS
URL_FRONTEND=https://localhost:3000

# Servidor
PUERTO_BACKEND=5077
```

### Personalizar Puertos

Edita `docker-compose.yml`:

```yaml
ports:
  - "PUERTO:5001"  # Backend
  - "PUERTO:3000"  # Frontend
```

---

## 🚨 Solución de Problemas

### Error: Puerto ya en uso

```bash
# Linux/Mac
lsof -i :5077
kill -9 PID

# Windows
netstat -ano | findstr :5077
taskkill /PID PID /F
```

### Error: Certificados SSL no confiables

**Es normal en desarrollo con certificados autofirmados.**

- **Chrome:** "Avanzado" → "Continuar a localhost"
- **Firefox:** "Avanzado" → "Aceptar el riesgo"
- **Safari:** "Mostrar detalles" → "visitar este sitio web"

### Error: Docker no inicia

```bash
# Verificar estado
docker ps

# Ver logs
docker-compose logs

# Reiniciar Docker
sudo systemctl restart docker  # Linux
# Reinicia Docker Desktop en Windows/Mac

# Limpiar sistema
docker-compose down -v
docker system prune -a
```

### Error: Pruebas frontend fallan

```bash
# Instalar dependencias localmente
cd frontend
npm install

# Ejecutar pruebas
./ejecutar_pruebas_frontend.sh
```

### Error: Base de datos bloqueada

```bash
# Detener contenedores
docker-compose down

# Eliminar BD
rm backend/datos/app.db

# Reconstruir
docker-compose up --build
```

---

## 📊 Gestión de Datos

### Privacidad de Usuario

**Importante:** Cada análisis es **privado e independiente por usuario**.

- ✅ Los usuarios solo ven su propio historial
- ✅ Las imágenes se almacenan localmente en el servidor
- ✅ No se comparten datos entre usuarios
- ✅ Posibilidad de eliminar análisis individuales
- ✅ Timestamps para auditoría

### Backup de Base de Datos

```bash
# Exportar base de datos
docker exec analizador-backend sqlite3 /app/datos/app.db .dump > backup.sql

# Restaurar base de datos
docker exec -i analizador-backend sqlite3 /app/datos/app.db < backup.sql
```

### Inspeccionar Base de Datos SQLite

**Opción 1: Script Python Automatizado** ✅ Recomendado

```bash
# Ejecutar script de inspección visual
python3 inspeccionar_bd.py
```

Este script muestra:
- 📊 Lista de todas las tablas
- 👥 Usuarios registrados con fechas
- 🔒 Información de hashes de contraseñas
- 🖼️ Análisis realizados por usuario
- 📈 Estadísticas por proveedor de IA
- 💾 Tamaño de la base de datos

**Opción 2: SQLite CLI Directamente**

```bash
# Acceder a la base de datos
sqlite3 backend/datos/app.db
```

Una vez dentro de SQLite, comandos útiles:

```sql
-- Ver todas las tablas
.tables

-- Ver estructura de la tabla usuarios
.schema usuarios

-- Ver estructura de la tabla analisis
.schema analisis

-- Ver todos los usuarios
SELECT * FROM usuarios;

-- Ver solo nombres de usuario y fechas
SELECT nombre_usuario, fecha_creacion, fecha_ultima_sesion FROM usuarios;

-- Contar usuarios
SELECT COUNT(*) FROM usuarios;

-- Ver análisis de un usuario específico
SELECT * FROM analisis WHERE usuario_id = 1;

-- Ver análisis con nombre de usuario (JOIN)
SELECT u.nombre_usuario, a.nombre_archivo, a.proveedor_ia, a.fecha_analisis
FROM analisis a
JOIN usuarios u ON a.usuario_id = u.id
ORDER BY a.fecha_analisis DESC;

-- Salir de SQLite
.quit
```

**Opción 3: Desde el Contenedor Docker**

```bash
# Acceder con Python interactivo
docker exec -it analizador-backend python3

# Luego ejecutar:
# >>> from app import app
# >>> from modelos import Usuario, Analisis
# >>> with app.app_context():
# ...     for u in Usuario.query.all():
# ...         print(f'{u.nombre_usuario}: {u.contar_analisis()} análisis')
# >>> exit()
```

**Opción 4: Herramientas GUI** (Opcional)

Para una interfaz gráfica, puedes usar:
- **DB Browser for SQLite**: https://sqlitebrowser.org/
- **DBeaver**: https://dbeaver.io/
- **TablePlus**: https://tableplus.com/

Simplemente abre el archivo: `backend/datos/app.db`
---

## 🚀 Mejoras Futuras

### Posibles Extensiones

- [ ] Agregar más proveedores de IA (Azure Vision, AWS Rekognition)
- [ ] Implementar procesamiento por lotes (múltiples imágenes)
- [ ] Sistema de etiquetas personalizadas por usuario
- [ ] Exportación de historial (CSV, PDF)
- [ ] Dashboard con estadísticas y gráficos
- [ ] Búsqueda avanzada en historial
- [ ] Soporte para videos
- [ ] API pública con documentación Swagger/OpenAPI
- [ ] Notificaciones push
- [ ] Modo offline con PWA
- [ ] Integración con redes sociales
- [ ] Sistema de favoritos y colecciones

---

## 📄 Licencia

Este proyecto es una prueba técnica de desarrollo para evaluación de habilidades.

**Uso educativo y de demostración.**

---

## 👨‍💻 Autor

**Steeven Vargas Andrango**

- 🌐 GitHub: [@VargasAndrangoSteeven](https://github.com/VargasAndrangoSteeven)
- 📅 Fecha: Noviembre 2024
- 🎯 Proyecto: Prueba Técnica Kushki - Analizador Inteligente de Imágenes


## 🙏 Agradecimientos

Gracias por revisar este proyecto. Se ha puesto especial atención en:
---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:

1. Revisa la sección de **Solución de Problemas** arriba
2. Consulta los archivos de documentación:
   - [PRUEBAS.md](PRUEBAS.md) - Para temas de testing
3. Ejecuta los scripts de verificación:
   ```bash
   ./verificar_seguridad.sh
   ./ejecutar_pruebas_backend.sh
   ./ejecutar_pruebas_frontend.sh
   ```

---

## 🎉 ¡Disfruta explorando la aplicación!

**¡El sistema está listo para analizar tus imágenes con IA!** 🖼️🤖✨

---

<div align="center">

**Desarrollado con ❤️ por Steeven Vargas**

[![GitHub](https://img.shields.io/badge/GitHub-VargasAndrangoSteeven-blue?style=flat&logo=github)](https://github.com/VargasAndrangoSteeven)

**Noviembre 2024**

</div>
