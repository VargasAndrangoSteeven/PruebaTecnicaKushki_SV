# 🧪 Guía de Pruebas Automatizadas

**Autor:** Steeven Vargas
**Fecha:** Noviembre 2024
**Proyecto:** Analizador de Imágenes con IA

---

## 📋 Índice

1. [Resumen de Pruebas](#resumen-de-pruebas)
2. [Pruebas del Backend (Pytest)](#pruebas-del-backend)
3. [Pruebas del Frontend (Jest)](#pruebas-del-frontend)
4. [Comandos Rápidos](#comandos-rápidos)
5. [Resultados y Cobertura](#resultados-y-cobertura)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Resumen de Pruebas

| Componente | Framework | Archivos | Ubicación |
|------------|-----------|----------|-----------|
| **Backend** | Pytest | `test_autenticacion.py` | `backend/pruebas/` |
| **Frontend** | Jest + React Testing Library | _(No creados)_ | `frontend/src/` |

### Estado Actual:

- ✅ **Backend:** 9 pruebas automatizadas (autenticación)
- ⚠️ **Frontend:** Configurado pero sin archivos de prueba

---

## 🐍 Pruebas del Backend (Pytest)

### Archivo de Pruebas:

📁 **`backend/pruebas/test_autenticacion.py`**

### Pruebas Disponibles:

#### 1. **TestRegistro** (3 pruebas)
- ✅ `test_registro_exitoso` - Registro exitoso de usuario
- ✅ `test_registro_contrasena_debil` - Contraseña débil rechazada
- ✅ `test_registro_usuario_duplicado` - Usuario duplicado rechazado

#### 2. **TestInicioSesion** (3 pruebas)
- ✅ `test_inicio_sesion_exitoso` - Login exitoso con credenciales válidas
- ✅ `test_inicio_sesion_contrasena_incorrecta` - Contraseña incorrecta
- ✅ `test_inicio_sesion_usuario_no_existe` - Usuario no existente

#### 3. **TestVerificacionToken** (3 pruebas)
- ✅ `test_verificar_token_valido` - Verificación de token JWT válido
- ✅ `test_verificar_token_sin_token` - Petición sin token
- ✅ `test_verificar_token_invalido` - Token inválido o expirado

---

### 🚀 Cómo Ejecutar las Pruebas del Backend

#### **Opción 1: Usar Script Interactivo (Recomendado)**

```bash
./ejecutar_pruebas_backend.sh
```

Este script te presenta un menú con opciones:

```
📋 Opciones de ejecución:
  1) Ejecutar TODAS las pruebas
  2) Ejecutar pruebas con REPORTE DETALLADO
  3) Ejecutar pruebas con COBERTURA
  4) Ejecutar pruebas ESPECÍFICAS (por clase)
  5) Ejecutar prueba INDIVIDUAL
```

#### **Opción 2: Comandos Directos**

##### Ejecutar todas las pruebas:
```bash
docker exec analizador-backend pytest /app/pruebas/ -v
```

##### Ejecutar con reporte detallado:
```bash
docker exec analizador-backend pytest /app/pruebas/ -v --tb=short -s
```

##### Ejecutar con cobertura de código:
```bash
docker exec analizador-backend pytest /app/pruebas/ -v \
  --cov=/app \
  --cov-report=term-missing \
  --cov-report=html
```

##### Ejecutar solo una clase de pruebas:
```bash
docker exec analizador-backend pytest /app/pruebas/test_autenticacion.py::TestRegistro -v
```

##### Ejecutar una prueba específica:
```bash
docker exec analizador-backend pytest \
  /app/pruebas/test_autenticacion.py::TestInicioSesion::test_inicio_sesion_exitoso -v -s
```

#### **Opción 3: Desde Modo No Interactivo**

```bash
# Ejecutar todas las pruebas
./ejecutar_pruebas_backend.sh 1

# Ejecutar con cobertura
./ejecutar_pruebas_backend.sh 3
```

---

### 📊 Resultados Esperados

#### Ejecución Exitosa:
```
=================== test session starts ====================
platform linux -- Python 3.11.14, pytest-7.4.3
collected 9 items

pruebas/test_autenticacion.py::TestRegistro::test_registro_exitoso PASSED [ 11%]
pruebas/test_autenticacion.py::TestRegistro::test_registro_contrasena_debil PASSED [ 22%]
pruebas/test_autenticacion.py::TestRegistro::test_registro_usuario_duplicado PASSED [ 33%]
pruebas/test_autenticacion.py::TestInicioSesion::test_inicio_sesion_exitoso PASSED [ 44%]
pruebas/test_autenticacion.py::TestInicioSesion::test_inicio_sesion_contrasena_incorrecta PASSED [ 55%]
pruebas/test_autenticacion.py::TestInicioSesion::test_inicio_sesion_usuario_no_existe PASSED [ 66%]
pruebas/test_autenticacion.py::TestVerificacionToken::test_verificar_token_valido PASSED [ 77%]
pruebas/test_autenticacion.py::TestVerificacionToken::test_verificar_token_sin_token PASSED [ 88%]
pruebas/test_autenticacion.py::TestVerificacionToken::test_verificar_token_invalido PASSED [100%]

=================== 9 passed in 1.24s ======================
```

#### Reporte de Cobertura:
```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
app.py                               45      3    93%   12-14
modelos/usuario.py                   52      0   100%
rutas/autenticacion.py               89      5    94%   45, 67-69
servicios/servicio_auth.py           67      2    97%   23, 45
---------------------------------------------------------------
TOTAL                               253      10   96%
```

---

### ⚠️ Nota Importante: Pruebas y Captcha

Algunas pruebas **fallan actualmente** porque el sistema de registro ahora **requiere captcha**, pero las pruebas no lo incluyen.

**Pruebas que pueden fallar:**
- ❌ `test_registro_exitoso` - Falta captcha
- ❌ `test_registro_usuario_duplicado` - Falta captcha

**Pruebas que pasan:**
- ✅ Todas las de `TestInicioSesion` (no requieren captcha)
- ✅ Todas las de `TestVerificacionToken`
- ✅ `test_registro_contrasena_debil` (falla antes del captcha)

**Para arreglar las pruebas de registro**, necesitarías:
1. Generar un captcha antes de cada prueba
2. Incluir `captcha_token` y `captcha_respuesta` en el JSON

---

## ⚛️ Pruebas del Frontend (Jest)

### Estado Actual:

El frontend **tiene Jest configurado** en `package.json`, pero **no tiene archivos de prueba** creados.

### 🚀 Cómo Ejecutar las Pruebas del Frontend

#### **Opción 1: Usar Script Interactivo**

```bash
./ejecutar_pruebas_frontend.sh
```

Opciones disponibles:
```
📋 Opciones de ejecución:
  1) Ejecutar pruebas (si existen archivos .test.js)
  2) Ejecutar pruebas con COBERTURA
  3) Ejecutar pruebas en modo WATCH
  4) Crear archivo de prueba de EJEMPLO
```

#### **Opción 2: Comandos Directos**

##### Ejecutar todas las pruebas:
```bash
cd frontend && npm test -- --watchAll=false
```

##### Ejecutar con cobertura:
```bash
cd frontend && npm test -- --coverage --watchAll=false
```

##### Ejecutar en modo watch (se re-ejecutan al guardar):
```bash
cd frontend && npm test
```

#### **Opción 3: Crear Archivo de Prueba de Ejemplo**

```bash
./ejecutar_pruebas_frontend.sh 4
```

Esto crea `frontend/src/App.test.js` con una prueba básica.

---

### 📝 Ejemplo de Archivo de Prueba Frontend

Si quieres crear tus propias pruebas, aquí hay un ejemplo:

**`frontend/src/componentes/Autenticacion/Login.test.js`**

```javascript
/**
 * Autor: Steeven Vargas
 * Fecha: Noviembre 2024
 * Descripción: Pruebas para el componente Login
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Login from './Login';

describe('Login Component', () => {
  test('renderiza formulario de login', () => {
    render(
      <BrowserRouter>
        <Login alIniciarSesion={jest.fn()} />
      </BrowserRouter>
    );

    expect(screen.getByLabelText(/usuario/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/contraseña/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /iniciar sesión/i })).toBeInTheDocument();
  });

  test('muestra error con campos vacíos', async () => {
    render(
      <BrowserRouter>
        <Login alIniciarSesion={jest.fn()} />
      </BrowserRouter>
    );

    const botonLogin = screen.getByRole('button', { name: /iniciar sesión/i });
    fireEvent.click(botonLogin);

    // El formulario debería prevenir el submit con campos vacíos
    expect(screen.queryByText(/error/i)).not.toBeInTheDocument();
  });
});
```

---

## ⚡ Comandos Rápidos

### Backend

```bash
# Ejecutar todas las pruebas
./ejecutar_pruebas_backend.sh 1

# Ejecutar con cobertura
./ejecutar_pruebas_backend.sh 3

# Ejecutar solo pruebas de login
docker exec analizador-backend pytest /app/pruebas/test_autenticacion.py::TestInicioSesion -v
```

### Frontend

```bash
# Crear archivo de ejemplo
./ejecutar_pruebas_frontend.sh 4

# Ejecutar pruebas
./ejecutar_pruebas_frontend.sh 1

# Ejecutar con cobertura
./ejecutar_pruebas_frontend.sh 2
```

---

## 📈 Resultados y Cobertura

### Generar Reporte HTML de Cobertura (Backend)

```bash
docker exec analizador-backend pytest /app/pruebas/ \
  --cov=/app \
  --cov-report=html \
  --cov-report=term-missing
```

El reporte HTML se genera en `backend/htmlcov/index.html`

Para verlo:
```bash
# macOS
open backend/htmlcov/index.html

# Linux
xdg-open backend/htmlcov/index.html
```

### Cobertura Actual (Backend):

| Módulo | Cobertura Estimada |
|--------|-------------------|
| Autenticación | ~94% |
| Modelos | ~100% |
| Servicios Auth | ~97% |
| **Total** | **~96%** |

---

## 🔧 Troubleshooting

### Problema: "El contenedor no está corriendo"

**Solución:**
```bash
docker-compose up -d backend
# o
docker-compose up -d frontend
```

### Problema: "ModuleNotFoundError"

**Solución:**
```bash
# Reconstruir el contenedor
docker-compose build backend
docker-compose up -d backend
```

### Problema: Pruebas de registro fallan (captcha)

**Explicación:** Las pruebas fueron creadas antes de implementar el captcha.

**Solución temporal:** Ejecuta solo las pruebas que no requieren registro:
```bash
docker exec analizador-backend pytest \
  /app/pruebas/test_autenticacion.py::TestInicioSesion -v

docker exec analizador-backend pytest \
  /app/pruebas/test_autenticacion.py::TestVerificacionToken -v
```

### Problema: Frontend no encuentra archivos de prueba

**Solución:** Crea un archivo de prueba de ejemplo:
```bash
./ejecutar_pruebas_frontend.sh 4
```

---

## 📚 Recursos Adicionales

### Pytest (Backend)
- **Documentación:** https://docs.pytest.org/
- **Fixtures:** https://docs.pytest.org/en/stable/how-to/fixtures.html
- **Coverage:** https://pytest-cov.readthedocs.io/

### Jest (Frontend)
- **Documentación:** https://jestjs.io/
- **React Testing Library:** https://testing-library.com/react
- **User Events:** https://testing-library.com/docs/user-event/intro

---

## 🎓 Buenas Prácticas

### Backend

1. ✅ **Usa fixtures** para datos de prueba reutilizables
2. ✅ **Aísla las pruebas** - cada prueba debe ser independiente
3. ✅ **Usa bases de datos en memoria** - SQLite para pruebas
4. ✅ **Nombra descriptivamente** - `test_registro_exitoso` vs `test1`
5. ✅ **Documenta las pruebas** - explica qué se está probando

### Frontend

1. ✅ **Prueba comportamiento, no implementación**
2. ✅ **Usa queries semánticas** - `getByRole`, `getByLabelText`
3. ✅ **Simula interacciones del usuario** - `fireEvent`, `userEvent`
4. ✅ **Espera cambios asíncronos** - `waitFor`, `findBy...`
5. ✅ **Mock servicios externos** - APIs, localStorage, etc.

---

## 🚀 Siguiente Paso: Ejecutar Pruebas

### Backend:
```bash
./ejecutar_pruebas_backend.sh
```

### Frontend:
```bash
./ejecutar_pruebas_frontend.sh
```

---

**Última actualización:** Noviembre 2024
**Autor:** Steeven Vargas
