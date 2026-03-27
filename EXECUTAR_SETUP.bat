@echo off
REM =============================================================================
REM SETUP COMPLETO - SISTEMA DE ESTOQUE COM MYSQL
REM Execute este arquivo para configurar tudo automaticamente
REM =============================================================================

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║              SETUP COMPLETO - SISTEMA DE ESTOQUE                          ║
echo ║                       MySQL + Dependências                                ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ ERRO: Python não está instalado ou não está no PATH!
    echo.
    echo Para usar este sistema, você precisa:
    echo 1. Instalar Python 3.6+ em https://www.python.org
    echo 2. Marcar "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
)

echo ✓ Python encontrado
python --version
echo.

REM Executar setup completo
echo Iniciando setup automático...
echo.

python setup_completo.py

if %errorlevel% neq 0 (
    echo.
    echo ✗ Erro durante o setup
    echo.
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║                    SETUP CONCLUÍDO COM SUCESSO!                           ║
echo ║                                                                           ║
echo ║  Próximo passo: execute "python app.py"                                   ║
echo ║  Acesse em seu navegador: http://localhost:5000                           ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.

pause
