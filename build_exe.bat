@echo off
REM =============================================================================
REM SCRIPT PARA CRIAR EXECUTÁVEL DO SISTEMA DE ESTOQUE
REM =============================================================================

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║           CRIANDO EXECUTÁVEL - SISTEMA DE ESTOQUE                       ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se estamos no ambiente virtual
if not defined VIRTUAL_ENV (
    echo ✗ ERRO: Ative o ambiente virtual primeiro!
    echo Execute: .venv\Scripts\activate
    pause
    exit /b 1
)

echo ✓ Ambiente virtual ativado

REM Instalar dependências se necessário
echo Verificando dependências...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ✗ Erro ao instalar dependências
    pause
    exit /b 1
)
echo ✓ Dependências instaladas

REM Limpar builds anteriores
echo Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"
echo ✓ Builds anteriores limpos

REM Criar executável com PyInstaller
echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║                       CRIANDO EXECUTÁVEL...                            ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.

pyinstaller --onefile --windowed ^
    --name="SistemaEstoque" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "estoque.db;." ^
    --hidden-import flask ^
    --hidden-import flask_sqlalchemy ^
    --hidden-import sqlalchemy ^
    --hidden-import werkzeug ^
    --hidden-import sqlite3 ^
    launcher.py

if %errorlevel% neq 0 (
    echo ✗ Erro ao criar executável
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║                       EXECUTÁVEL CRIADO COM SUCESSO!                    ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.
echo O executável foi criado em: dist\SistemaEstoque.exe
echo.
echo Para usar:
echo 1. Copie o arquivo SistemaEstoque.exe para onde desejar
echo 2. Execute o arquivo (não precisa instalar Python)
echo 3. O sistema abrirá automaticamente no navegador
echo.
echo Pressione qualquer tecla para continuar...
pause >nul