#!/bin/bash

# --- VARIABLES Y CONFIGURACIÓN ---
CONTAINER_NAME="bio_mongo"
# RUTA de persistencia: se crea en el directorio actual (./)
DB_DATA_PATH="./T1-MongoDB/mongo_data"
VENV_PATH="./venv"

echo "======================================================"
echo "🚀 INGENIERÍA BIOINFORMÁTICA: SETUP (Linux/macOS)"
echo "======================================================"

# Nota: Se asume que requirements.txt ya existe.

# --- 1. CONFIGURACIÓN DEL ENTORNO PYTHON ---
echo "🐍 Creando y activando entorno virtual en $VENV_PATH..."
python3 -m venv $VENV_PATH
source $VENV_PATH/bin/activate

echo "📦 Instalando dependencias desde requirements.txt..."
# Se asume que requirements.txt es un archivo estático preexistente
pip install -r requirements.txt

# --- 2. CONFIGURACIÓN DE MONGODB EN DOCKER ---
echo "🐳 Configurando MongoDB en Docker..."

# A. Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "🚨 ERROR: Docker no se está ejecutando o no tienes permisos (prueba con 'sudo systemctl start docker')."
    echo "⚠️ La instalación de Python está completa, pero el servidor DB no se iniciará."
    exit 1
fi

# B. Crear volumen persistente local (en el directorio del proyecto)
echo "📁 Creando volumen persistente en $DB_DATA_PATH..."
mkdir -p $DB_DATA_PATH

# C. Detener y eliminar contenedor antiguo (si existe)
if docker ps -a | grep -q $CONTAINER_NAME; then
    echo "🗑️ Contenedor antiguo '$CONTAINER_NAME' encontrado. Deteniendo y eliminando..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# D. Iniciar nuevo contenedor con volumen persistente
# Importante: Se mapea la ruta local DB_DATA_PATH al directorio interno de Mongo (/data/db)
echo "▶️ Iniciando nuevo contenedor MongoDB (bio_mongo) en localhost:27017 con datos persistentes locales..."
docker run -d -p 27017:27017 \
    -v $(pwd)/mongo_data:/data/db \
    --name $CONTAINER_NAME mongo:latest

# --- 3. VERIFICACIÓN FINAL ---
echo "======================================================"
echo "✅ SETUP COMPLETADO."
echo "   - Para usar el entorno: source $VENV_PATH/bin/activate"
echo "   - Conexión DB: localhost:27017 (Contenedor: $CONTAINER_NAME)"
echo "   - Directorio de datos DB: $DB_DATA_PATH"
echo "======================================================"
