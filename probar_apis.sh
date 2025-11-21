#!/bin/bash

# Script de prueba de APIs
echo "========================================="
echo "PRUEBA DE APIs - Analizador de Imágenes"
echo "========================================="
echo ""

# 1. Login
echo "1️⃣  Probando login..."
TOKEN_RESPONSE=$(curl -k -s -X POST 'https://localhost:5001/api/auth/iniciar-sesion' \
  -H 'Content-Type: application/json' \
  -d '{"nombre_usuario":"admin2025","contrasena":"pass2025"}')

TOKEN=$(echo $TOKEN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('datos', {}).get('token', ''))")

if [ -z "$TOKEN" ]; then
    echo "❌ Error al obtener token"
    echo $TOKEN_RESPONSE | python3 -m json.tool
    exit 1
fi

echo "✅ Login exitoso"
echo "Token: ${TOKEN:0:50}..."
echo ""

# 2. Descargar imagen de prueba
echo "2️⃣  Descargando imagen de prueba..."
curl -s -o /tmp/test_image.jpg "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400"
echo "✅ Imagen descargada: /tmp/test_image.jpg"
echo ""

# 3. Probar análisis con Google Vision
echo "3️⃣  Probando Google Vision API..."
GOOGLE_RESPONSE=$(curl -k -s -X POST 'https://localhost:5001/api/analizar' \
  -H "Authorization: Bearer $TOKEN" \
  -F "imagen=@/tmp/test_image.jpg" \
  -F "descripcion=Gato de prueba" \
  -F "tipo_ia=google")

echo "$GOOGLE_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data.get('exito'):
        print('✅ Google Vision funciona correctamente')
        print('   Etiquetas encontradas:', len(data.get('datos', {}).get('etiquetas', [])))
    else:
        print('❌ Error:', data.get('mensaje'))
        print(json.dumps(data, indent=2))
except Exception as e:
    print('❌ Error al procesar respuesta:', e)
    print(sys.stdin.read())
"
echo ""

# 4. Probar análisis con Imagga
echo "4️⃣  Probando Imagga API..."
IMAGGA_RESPONSE=$(curl -k -s -X POST 'https://localhost:5001/api/analizar' \
  -H "Authorization: Bearer $TOKEN" \
  -F "imagen=@/tmp/test_image.jpg" \
  -F "descripcion=Gato de prueba con Imagga" \
  -F "tipo_ia=imagga")

echo "$IMAGGA_RESPONSE" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data.get('exito'):
        print('✅ Imagga API funciona correctamente')
        print('   Etiquetas encontradas:', len(data.get('datos', {}).get('etiquetas', [])))
    else:
        print('❌ Error:', data.get('mensaje'))
        print(json.dumps(data, indent=2))
except Exception as e:
    print('❌ Error al procesar respuesta:', e)
    print(sys.stdin.read())
"
echo ""

# 5. Verificar historial
echo "5️⃣  Verificando historial..."
HISTORIAL=$(curl -k -s -X GET 'https://localhost:5001/api/historial' \
  -H "Authorization: Bearer $TOKEN")

echo "$HISTORIAL" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if data.get('exito'):
        total = len(data.get('datos', []))
        print(f'✅ Historial funciona: {total} análisis registrados')
    else:
        print('❌ Error:', data.get('mensaje'))
except Exception as e:
    print('❌ Error:', e)
"
echo ""

echo "========================================="
echo "PRUEBA COMPLETADA"
echo "========================================="
