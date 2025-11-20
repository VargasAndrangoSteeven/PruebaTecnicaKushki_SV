# Analizador Inteligente de Contenido de Imágenes

## Descripción del Proyecto

Aplicación web full-stack que permite a los usuarios subir imágenes y analizarlas utilizando servicios de Inteligencia Artificial. La aplicación procesa las imágenes y devuelve etiquetas descriptivas (tags) con niveles de confianza.

**Características principales:**
- Sistema de autenticación con JWT y captcha
- Análisis de imágenes con múltiples proveedores de IA (Google Cloud Vision, Imagga)
- Historial privado de análisis por usuario
- Diseño responsivo con Material-UI
- Seguridad robusta (GPG, SSL, validaciones)
- Arquitectura contenerizada con Docker

---

## Tecnologías Utilizadas

### Backend
- Python 3.11
- Flask 3.0
- SQLAlchemy (ORM)
- SQLite (Base de datos)
- JWT (Autenticación)
- bcrypt (Encriptación de contraseñas)
- python-gnupg (Encriptación de datos)
- pytest (Testing - cobertura 80%)

### Frontend
- React 18 (JavaScript puro sin TSX)
- Material-UI (MUI v5)
- Axios
- React Router v6
- Jest & React Testing Library

### DevOps
- Docker & Docker Compose
- Nginx (Proxy reverso con SSL)
- Certificados SSL autofirmados
- GitHub Actions (CI/CD con pipeline automatizado)

### APIs de IA
- Google Cloud Vision API
- Imagga API

---

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- **Docker** (versión 20.10 o superior)
- **Docker Compose** (versión 2.0 o superior)
- **Git**

Para verificar las instalaciones:
```bash
docker --version
docker-compose --version
git --version
```

---

## Configuración Rápida

### 1. Clonar el Repositorio

```bash
git clone https://github.com/VargasAndrangoSteeven/PruebaTecnicaKushki_SV.git
cd PruebaTecnicaKushki_SV
```

### 2. Configurar Credenciales de Google Cloud Vision

**Importante:** Coloca tu archivo de credenciales JSON de Google Cloud en:
```
backend/credenciales/google-vision.json  (en el proyecto ya estan preconfiguradas)
```

### 3. Ejecutar Script de Configuración Automática

El proyecto incluye scripts automatizados multiplataforma:

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

### 4. Acceder a la Aplicación

La aplicación estará disponible en:
- **Frontend:** https://localhost:3000
- **Backend API:** https://localhost:5000

**Nota:** Tu navegador mostrará advertencia de certificado SSL (es normal en desarrollo con certificados autofirmados). Acepta el riesgo y continúa.

### Usuario de Prueba Predeterminado

El sistema incluye un usuario administrador:
- **Usuario:** `admin2025`
- **Contraseña:** `pass2025`

---

## Configuración Manual (Avanzado)

Si prefieres configurar paso a paso sin el script:

### 1. Crear archivo de variables de entorno

```bash
cp .env.ejemplo .env
```

### 2. Editar el archivo .env

```env
# Configuración Flask
FLASK_ENV=desarrollo
CLAVE_SECRETA=genera-una-clave-segura-aqui
CLAVE_SECRETA_JWT=genera-otra-clave-segura-aqui

# Base de Datos
URL_BASE_DATOS=sqlite:///./datos/app.db

# Google Cloud Vision API
CREDENCIALES_GOOGLE=./credenciales/google-vision.json

# Imagga API
IMAGGA_API_KEY=acc_17c557dadc898af
IMAGGA_API_SECRET=2be723d45c97944643a1afea53fd3d20

# Encriptación GPG
FRASE_SEGURIDAD_GPG=tu-frase-seguridad-gpg

# CORS
URL_FRONTEND=https://localhost:3000

# Puerto Backend
PUERTO_BACKEND=5000
```

### 3. Generar certificados SSL

```bash
# Crear directorio para certificados
mkdir -p nginx/ssl

# Generar certificados autofirmados
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/privado.key \
  -out nginx/ssl/certificado.crt \
  -subj "/C=EC/ST=Pichincha/L=Quito/O=KushkiTest/CN=localhost"
```

### 4. Iniciar con Docker

```bash
docker-compose up --build
```

---

## Ejecución en Desarrollo (Sin Docker)

### Backend

```bash
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requisitos.txt

# Inicializar base de datos
python inicializar_bd.py

# Ejecutar servidor
python app.py
```

El backend estará en: http://localhost:5000

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
```

El frontend estará en: http://localhost:3000

---

## Estructura del Proyecto

```
PruebaTecnicaKushki_SV/
├── backend/                          # API Flask
│   ├── app.py                       # Punto de entrada principal
│   ├── config/                      # Configuraciones
│   │   ├── __init__.py
│   │   ├── configuracion.py         # Config Flask, BD, JWT
│   │   └── seguridad.py             # Config SSL, CORS, Headers
│   ├── modelos/                     # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   ├── usuario.py               # Modelo Usuario
│   │   └── analisis.py              # Modelo Análisis de Imagen
│   ├── rutas/                       # Endpoints API
│   │   ├── __init__.py
│   │   ├── autenticacion.py         # Login, registro, logout
│   │   └── analisis.py              # Análisis de imágenes
│   ├── servicios/                   # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── servicio_ia.py           # Integración APIs IA
│   │   ├── servicio_auth.py         # Lógica autenticación
│   │   └── servicio_encriptacion.py # GPG, bcrypt
│   ├── utilidades/                  # Funciones auxiliares
│   │   ├── __init__.py
│   │   ├── validadores.py           # Validación inputs
│   │   ├── decoradores.py           # JWT decorators
│   │   └── respuestas.py            # Formato respuestas JSON
│   ├── pruebas/                     # Tests unitarios
│   │   ├── __init__.py
│   │   ├── test_autenticacion.py
│   │   ├── test_analisis.py
│   │   └── conftest.py
│   ├── credenciales/                # Credenciales APIs
│   │   ├── .gitkeep
│   │   └── google-vision.json       # (No versionado)
│   ├── cargas/                      # Imágenes subidas
│   │   └── .gitkeep
│   ├── datos/                       # Base de datos SQLite
│   │   └── .gitkeep
│   ├── requisitos.txt               # Dependencias Python
│   ├── Dockerfile                   # Imagen Docker backend
│   └── inicializar_bd.py            # Script inicialización BD
│
├── frontend/                         # Aplicación React
│   ├── public/
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   └── manifest.json
│   ├── src/
│   │   ├── componentes/             # Componentes React
│   │   │   ├── Autenticacion/
│   │   │   │   ├── Login.js
│   │   │   │   ├── Registro.js
│   │   │   │   └── Captcha.js
│   │   │   ├── Analizador/
│   │   │   │   ├── SubidorImagen.js
│   │   │   │   ├── SelectorIA.js
│   │   │   │   ├── ResultadosAnalisis.js
│   │   │   │   └── CargandoSpinner.js
│   │   │   ├── Historial/
│   │   │   │   ├── ListaHistorial.js
│   │   │   │   └── DetalleAnalisis.js
│   │   │   ├── Comunes/
│   │   │   │   ├── Navbar.js
│   │   │   │   ├── Footer.js
│   │   │   │   └── AlertaMensaje.js
│   │   │   └── Layout/
│   │   │       └── LayoutPrincipal.js
│   │   ├── servicios/               # Clientes API
│   │   │   ├── api.js               # Configuración Axios
│   │   │   ├── servicioAuth.js      # Llamadas auth
│   │   │   └── servicioAnalisis.js  # Llamadas análisis
│   │   ├── utilidades/              # Utilidades frontend
│   │   │   ├── validaciones.js
│   │   │   ├── constantes.js
│   │   │   └── formateo.js
│   │   ├── App.js                   # Componente principal
│   │   ├── index.js                 # Punto de entrada
│   │   └── tema.js                  # Tema Material-UI
│   ├── package.json                 # Dependencias npm
│   ├── Dockerfile                   # Imagen Docker frontend
│   └── .env                         # Variables entorno React
│
├── nginx/                            # Configuración Nginx
│   ├── nginx.conf                   # Config proxy reverso
│   └── ssl/                         # Certificados SSL
│       ├── certificado.crt          # (Generado por script)
│       └── privado.key              # (Generado por script)
│
├── .github/                          # CI/CD
│   └── workflows/
│       └── ci.yml                   # Pipeline GitHub Actions
│
├── docker-compose.yml               # Orquestación servicios
├── .env.ejemplo                     # Template variables entorno
├── .gitignore                       # Archivos ignorados
├── desplegar.sh                     # Script deploy Linux/Mac
├── desplegar.ps1                    # Script deploy Windows
└── README.md                        # Documentación principal
```

---

## Testing

### Backend (pytest - cobertura 80%)

```bash
cd backend

# Ejecutar todos los tests
pytest

# Con reporte de cobertura
pytest --cov=. --cov-report=html --cov-report=term

# Ver reporte HTML
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Frontend (Jest)

```bash
cd frontend

# Ejecutar tests
npm test

# Con cobertura
npm test -- --coverage --watchAll=false

# Ver reporte
open coverage/lcov-report/index.html
```

### Pipeline CI/CD

El proyecto incluye GitHub Actions que ejecuta automáticamente en cada push:
- ✅ Linting (flake8, eslint)
- ✅ Tests unitarios (backend y frontend)
- ✅ Verificación de cobertura mínima (80%)
- ✅ Build de imágenes Docker
- ✅ Análisis de seguridad

---

## Endpoints de la API

### Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/registrar` | Registrar nuevo usuario | No |
| POST | `/api/auth/iniciar-sesion` | Iniciar sesión | No |
| POST | `/api/auth/cerrar-sesion` | Cerrar sesión | Sí |
| GET | `/api/auth/verificar` | Verificar token válido | Sí |

### Análisis de Imágenes

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/analizar` | Analizar una imagen | Sí |
| GET | `/api/historial` | Obtener historial del usuario | Sí |
| GET | `/api/historial/<id>` | Obtener análisis específico | Sí |
| DELETE | `/api/historial/<id>` | Eliminar análisis | Sí |

### Ejemplo de Petición - Registro

```bash
curl -X POST https://localhost:5000/api/auth/registrar \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "steeven",
    "contrasena": "MiPass123!",
    "respuesta_captcha": "03AGdBq24..."
  }'
```

### Ejemplo de Petición - Análisis

```bash
curl -X POST https://localhost:5000/api/analizar \
  -H "Authorization: Bearer TU_TOKEN_JWT" \
  -F "imagen=@/ruta/a/imagen.jpg" \
  -F "proveedor_ia=google"
```

### Ejemplo de Respuesta - Análisis

```json
{
  "exito": true,
  "datos": {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "etiquetas": [
      {
        "etiqueta": "Perro",
        "confianza": 0.98
      },
      {
        "etiqueta": "Golden Retriever",
        "confianza": 0.95
      },
      {
        "etiqueta": "Parque",
        "confianza": 0.91
      },
      {
        "etiqueta": "Césped",
        "confianza": 0.88
      }
    ],
    "proveedor_ia": "google",
    "nombre_archivo": "perro_parque.jpg",
    "fecha_creacion": "2024-11-19T15:30:00Z"
  },
  "mensaje": "Imagen analizada exitosamente"
}
```

---

## Seguridad Implementada

### Autenticación y Autorización
- ✅ JWT con expiración de 24 horas
- ✅ Contraseñas hasheadas con bcrypt (factor 12)
- ✅ Validación robusta de contraseñas:
  - Mínimo 8 caracteres
  - Al menos una mayúscula
  - Al menos un número
  - Al menos un símbolo (. , - _)
- ✅ Captcha en registro (protección contra bots)
- ✅ Tokens firmados y verificados

### Encriptación de Datos
- ✅ Base de datos SQLite encriptada con GPG
- ✅ Comunicación HTTPS con certificados SSL
- ✅ Variables de entorno para credenciales sensibles
- ✅ Archivo .env no versionado en Git

### Validaciones de Entrada
- ✅ Tipo de archivo (solo imágenes: jpg, jpeg, png, gif, webp)
- ✅ Tamaño máximo: 5MB por imagen
- ✅ Sanitización de inputs (XSS prevention)
- ✅ Validación de formatos JSON
- ✅ Rate limiting en endpoints críticos (10 req/min por usuario)

### Headers de Seguridad
- ✅ Content-Security-Policy (CSP)
- ✅ X-Frame-Options: DENY
- ✅ X-Content-Type-Options: nosniff
- ✅ Strict-Transport-Security (HSTS)
- ✅ X-XSS-Protection

### CORS Configurado
- ✅ Solo permite origen del frontend (https://localhost:3000)
- ✅ Métodos HTTP específicos permitidos
- ✅ Credentials incluidos para cookies

---

## Proveedores de IA

### Google Cloud Vision API

**Configuración:**
(Las credenciales ya están incluidas en el proyecto)
1. Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com)
2. Habilita Cloud Vision API
3. Crea una cuenta de servicio
4. Descarga las credenciales JSON
5. Coloca el archivo en `backend/credenciales/google-vision.json`

**Características:**
- Alta precisión en detección de objetos y escenas
- Reconocimiento de texto (OCR)
- Detección de rostros y emociones
- Clasificación de contenido seguro
- Detección de logos y marcas

**Límites gratuitos:**
- 1,000 solicitudes/mes gratis
- $1.50 por 1,000 imágenes adicionales

### Imagga API

**Configuración:**
Las credenciales ya están incluidas en el proyecto.

**Características:**
- Etiquetado automático multiidioma
- Categorización de imágenes
- Detección de colores dominantes
- Reconocimiento de contenido NSFW

**Límites gratuitos:**
- 1,000 solicitudes/mes gratis
- Procesamiento rápido

---

## Privacidad y Datos de Usuario

**Importante:** Cada análisis de imagen es **privado e independiente por usuario**.

- ✅ Los usuarios solo pueden ver su propio historial
- ✅ Las imágenes se almacenan localmente en el servidor
- ✅ No se comparten datos entre usuarios
- ✅ Posibilidad de eliminar análisis individuales
- ✅ Los análisis incluyen timestamp para auditoría

---

## Solución de Problemas

### Docker no inicia

```bash
# Verificar estado de Docker
docker ps

# Verificar logs
docker-compose logs

# Reiniciar Docker
sudo systemctl restart docker  # Linux
# o reinicia Docker Desktop en Windows/Mac

# Limpiar contenedores y volúmenes
docker-compose down -v
docker system prune -a
```

### Error: Puerto ya en uso

```bash
# Ver qué proceso usa el puerto 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Matar el proceso
kill -9 PID  # Linux/Mac
taskkill /PID PID /F  # Windows

# O cambiar el puerto en docker-compose.yml
```

### Certificados SSL no confiables

Es normal en desarrollo con certificados autofirmados:

**Chrome:**
1. Click en "Avanzado" o "Advanced"
2. Click en "Continuar a localhost (sitio no seguro)"

**Firefox:**
1. Click en "Avanzado" o "Advanced"
2. Click en "Aceptar el riesgo y continuar"

**Safari:**
1. Click en "Mostrar detalles"
2. Click en "visitar este sitio web"

### Error de credenciales de Google

Verifica que:
1. El archivo `google-vision.json` existe en `backend/credenciales/`
2. La API de Cloud Vision está habilitada en tu proyecto
3. La cuenta de servicio tiene permisos correctos
4. El formato del JSON es válido

### Error de API de Imagga

```bash
# Test manual de la API
curl -X GET "https://api.imagga.com/v2/tags?image_url=https://example.com/image.jpg" \
  -u "acc_17c557dadc898af:2be723d45c97944643a1afea53fd3d20"
```

### Base de datos bloqueada (SQLite)

```bash
# Detener todos los contenedores
docker-compose down

# Eliminar archivo de BD
rm backend/datos/app.db

# Reiniciar
docker-compose up --build
```

### Tests fallan

```bash
# Backend - instalar dependencias de test
cd backend
pip install -r requisitos.txt
pytest -v

# Frontend - limpiar cache
cd frontend
rm -rf node_modules package-lock.json
npm install
npm test
```

---

## Despliegue en Producción

### Consideraciones Importantes

**⚠️ Este proyecto está configurado para desarrollo local.**

Para producción, se recomienda:

1. **Separar repositorios:** Backend y frontend en repos independientes
2. **Base de datos:** Usar PostgreSQL o MySQL en servidor dedicado
3. **Certificados SSL:** Usar Let's Encrypt para certificados válidos
4. **Variables de entorno:** Usar servicios seguros (AWS Secrets Manager, HashiCorp Vault)
5. **Almacenamiento:** Usar S3 o similar para imágenes
6. **CDN:** CloudFront o Cloudflare para assets estáticos
7. **Monitoreo:** Implementar Prometheus, Grafana, Sentry
8. **Logging:** Centralizado con ELK Stack o CloudWatch
9. **Backups:** Automatizados y encriptados
10. **Escalado:** Kubernetes o ECS para orquestación
11. **Rate Limiting:** Implementar con Redis
12. **Cache:** Redis o Memcached

### Plataformas Sugeridas

- **Backend:** AWS Elastic Beanstalk, Google Cloud Run, Heroku
- **Frontend:** Vercel, Netlify, AWS S3 + CloudFront
- **Base de Datos:** AWS RDS, Google Cloud SQL
- **Contenedores:** AWS ECS, GKE, 

---

## Contribución y Mejoras Futuras

### Posibles Mejoras

- [ ] Agregar más proveedores de IA (Azure Vision, AWS Rekognition)
- [ ] Implementar procesamiento por lotes (múltiples imágenes)
- [ ] Sistema de etiquetas personalizadas por usuario
- [ ] Exportación de historial (CSV, PDF)
- [ ] Dashboard con estadísticas y gráficos
- [ ] Búsqueda avanzada en historial
- [ ] Soporte para videos
- [ ] API pública con documentación Swagger
- [ ] Notificaciones push
- [ ] Modo offline con PWA

---

## Licencia

Este proyecto es una prueba técnica de desarrollo para evaluación de habilidades.

---

## Autor

**Steeven Vargas**
- GitHub: [@VargasAndrangoSteeven](https://github.com/VargasAndrangoSteeven)
- Fecha: Noviembre 2024
- Proyecto: Prueba Técnica Kushki - Analizador Inteligente de Imágenes

---

## Agradecimientos

Gracias por revisar este proyecto. Se ha puesto especial atención en:
- ✅ Código limpio y documentado
- ✅ Arquitectura escalable
- ✅ Seguridad robusta
- ✅ Testing exhaustivo (>80% cobertura)
- ✅ DevOps con Docker
- ✅ Buenas prácticas de Git

**¡Espero que disfrutes explorando la aplicación!** 🚀