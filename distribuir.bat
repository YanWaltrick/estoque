@echo off
REM =============================================================================
REM SCRIPT PARA DISTRIBUIR O EXECUTÁVEL
REM =============================================================================

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║           DISTRIBUIÇÃO - SISTEMA DE ESTOQUE                            ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.

REM Criar pasta de distribuição
if not exist "distribuicao" mkdir distribuicao

echo Copiando arquivos...
copy "dist\SistemaEstoque.exe" "distribuicao\" >nul
copy "README_EXECUTAVEL.md" "distribuicao\README.md" >nul

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║                       DISTRIBUIÇÃO CRIADA!                             ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.
echo Arquivos criados em: distribuicao\
echo.
echo Conteúdo:
echo - SistemaEstoque.exe (17MB)
echo - README.md (instruções)
echo.
echo Para distribuir: copie a pasta 'distribuicao' inteira
echo.
pause