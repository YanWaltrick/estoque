@echo off
:: Script para executar o Sistema de Gestão de Estoque no Windows

title Sistema de Gestão de Estoque

echo.
echo ====================================================
echo  SISTEMA DE GESTAO DE ESTOQUE
echo ====================================================
echo.

:: Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python não está instalado ou não está no PATH.
    echo.
    echo Soluções:
    echo 1. Instale Python de: https://www.python.org/downloads/
    echo 2. Marque "Add Python to PATH" durante a instalação
    echo 3. Reinicie o computador
    echo.
    pause
    exit /b 1
)

echo [INFO] Python encontrado. Iniciando sistema...
echo.

:: Executa o programa principal
python estoque.py

:: Se houver erro, mostra mensagem
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Ocorreu um erro ao executar o sistema.
    echo.
    pause
    exit /b 1
)

pause
