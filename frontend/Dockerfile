# Dockerfile para Frontend React
FROM node:18-alpine as build

WORKDIR /app

# Copiar package.json
COPY package*.json ./

# Instalar dependencias (usar npm install en lugar de npm ci)
RUN npm install --production=false

# Copiar código fuente
COPY . .

# Construir aplicación
RUN npm run build

# Nginx para servir la aplicación
FROM nginx:alpine

# Configurar zona horaria
ENV TZ=America/Guayaquil
RUN apk add --no-cache tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Copiar build de React
COPY --from=build /app/build /usr/share/nginx/html

# Copiar configuración de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]