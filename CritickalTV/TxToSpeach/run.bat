@echo off
chcp 65001 >nul
REM Ruta por defecto si no se pasa argumento
SET "MODULO=src.main"
set PYTHONPATH=src
REM Si se pasa argumento, se usa como módulo
IF NOT "%~1"=="" (
    SET "MODULO=%~1"
)

echo 🟢 Ejecutando módulo: %MODULO%
python -m %MODULO%
