@echo off
REM =============================================================================
REM SCRIPT PARA INICIAR O FRONTEND WEB DO SISTEMA DE ESTOQUE
REM =============================================================================

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║           SISTEMA DE ESTOQUE - FRONTEND WEB                              ║
echo ║                     Iniciando Servidor...                                ║
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

REM Instalar dependências
echo Verificando dependências...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ✗ Erro ao instalar dependências
    pause
    exit /b 1
)
echo ✓ Dependências instaladas
echo.

REM Copiar dados de exemplo se não existir
if not exist "dados_estoque.json" (
    if exist "dados_estoque_exemplo.json" (
        echo Copiando dados de exemplo...
        copy "dados_estoque_exemplo.json" "dados_estoque.json" >nul
        echo ✓ Dados de exemplo copiados
    )
)
echo.

REM Iniciar a aplicação
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║                       INICIANDO SERVIDOR WEB                             ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.
echo O servidor será iniciado em: http://localhost:5000
echo.
echo Abra seu navegador e acesse: http://localhost:5000
echo.
echo Pressione CTRL+C para parar o servidor
echo.

python app.py
pause
