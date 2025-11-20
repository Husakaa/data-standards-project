@echo off
SET CONTAINER_NAME=bio_mongo
SET VENV_PATH=venv
:: La ruta de persistencia se establece dentro de la estructura T1-MongoDB/mongo_data
SET DB_DATA_FOLDER=T1-MongoDB\mongo_data
SET DB_DATA_PATH=%CD%\%DB_DATA_FOLDER%

echo ======================================================
echo 🚀 INGENIERÍA BIOINFORMÁTICA: SETUP (Windows Batch)
echo ======================================================

:: --- 1. CONFIGURACIÓN DEL ENTORNO PYTHON ---
echo 🐍 Creando entorno virtual en %VENV_PATH%...
:: Se usa 'python' asumiendo que está en el PATH de Windows
python -m venv %VENV_PATH%

echo 📦 Instalando dependencias desde requirements.txt...
:: Se asume que requirements.txt es un archivo estático preexistente.
:: Se activa el entorno virtual temporalmente para la instalación.
call %VENV_PATH%\Scripts\activate.bat
pip install -r requirements.txt
deactivate

:: --- 2. CONFIGURACIÓN DE MONGODB EN DOCKER ---
echo 🐳 Configurando MongoDB en Docker...

:: A. Verificar si Docker está corriendo (Check de disponibilidad)
docker info > NUL 2>&1
IF ERRORLEVEL 1 (
    echo 🚨 ERROR: Docker no se esta ejecutando o no esta disponible.
    echo ⚠️ La instalacion de Python esta completa, pero el servidor DB no se iniciara.
    GOTO :END
)

:: B. Crear volumen persistente local (en el directorio del proyecto)
echo 📁 Creando volumen persistente local en %DB_DATA_PATH%...
IF NOT EXIST "%DB_DATA_PATH%" mkdir "%DB_DATA_PATH%"

:: C. Detener y eliminar contenedor antiguo (si existe)
echo 🗑️ Intentando detener y eliminar contenedor antiguo %CONTAINER_NAME%...
docker stop %CONTAINER_NAME% > NUL 2>&1
docker rm %CONTAINER_NAME% > NUL 2>&1

:: D. Iniciar nuevo contenedor con volumen persistente
echo ▶️ Iniciando nuevo contenedor MongoDB (bio_mongo) en localhost:27017 con datos persistentes locales...
:: Se mapea la ruta absoluta de Windows al directorio interno de Mongo (/data/db)
docker run -d -p 27017:27017 ^
    -v "%DB_DATA_PATH%":/data/db ^
    --name %CONTAINER_NAME% mongo:latest

:: --- 3. VERIFICACIÓN FINAL ---
:END
echo ======================================================
echo ✅ SETUP COMPLETADO (Revisa la salida de Docker arriba).
echo    - Para usar el entorno: call %VENV_PATH%\Scripts\activate.bat
echo    - Conexión DB: localhost:27017 (Contenedor: %CONTAINER_NAME%)
echo    - Directorio de datos DB: %DB_DATA_PATH%
echo ======================================================
pause
