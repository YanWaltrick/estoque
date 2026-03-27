@echo off
REM =============================================================================
REM INICIAR SERVIDOR - SISTEMA DE ESTOQUE
REM =============================================================================

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║               SISTEMA DE ESTOQUE - SERVIDOR FLASK                         ║
echo ║                    Iniciando em http://localhost:5000                     ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ ERRO: Python não está instalado!
    echo.
    echo Por favor, instale Python de https://www.python.org
    echo E marque "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✓ Python encontrado
echo.

REM Verificar se dependências estão instaladas
python -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo ✗ Dependências não instaladas
    echo.
    echo Execute primeiro: setup_completo.py (ou EXECUTAR_SETUP.bat)
    echo.
    pause
    exit /b 1
)

echo ✓ Dependências encontradas
echo.

REM Iniciar servidor
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║                      SERVIDOR INICIANDO...                                ║
echo ║                                                                           ║
echo ║  Acesse em seu navegador: http://localhost:5000                           ║
echo ║                                                                           ║
echo ║  Login padrão:                                                            ║
echo ║    Usuário: admin                                                         ║
echo ║    Senha: admin                                                           ║
echo ║                                                                           ║
echo ║  Pressione CTRL+C para parar o servidor                                   ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.

python app.py

if %errorlevel% neq 0 (
    echo.
    echo ✗ Erro ao iniciar servidor
    echo.
    pause
    exit /b 1
)
