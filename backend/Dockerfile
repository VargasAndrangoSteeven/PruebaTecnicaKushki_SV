# 
# DOCKERFILE BACKEND - API Flask
# 
# Autor: Steeven Vargas
# Fecha: Noviembre 2024
# Descripción: Imagen Docker para el backend Python/Flask
# Base: Python 3.11 slim

FROM python:3.11-slim

# Metadata
LABEL maintainer="Steeven Vargas"
LABEL description="API Flask para Analizador Inteligente de Imágenes"
LABEL version="1.0"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TZ=America/Guayaquil

# Crear usuario no-root por seguridad
RUN useradd -m -u 1000 flask_user && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        curl \
        gnupg \
        libmagic1 \
        tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requisitos primero (mejor cache de Docker)
COPY requisitos.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install -r requisitos.txt

# Copiar código de la aplicación
COPY . .

# Dar permisos a la aplicación
RUN chown -R flask_user:flask_user /app

# Cambiar a usuario no-root
USER flask_user

# Exponer puerto
EXPOSE 5077

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5077/api/salud || exit 1

# Comando para iniciar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:5077", "--workers", "1", "--timeout", "120", "app:app"]
