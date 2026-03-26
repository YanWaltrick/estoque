@echo off
REM Instalador PostgreSQL - Sistema Estoque

echo.
echo ======================================
echo Instalador PostgreSQL v15
echo ======================================
echo.

REM Verificar se ja esta instalado
if exist "C:\Program Files\PostgreSQL\15\bin\psql.exe" (
    echo [OK] PostgreSQL ja esta instalado!
    "C:\Program Files\PostgreSQL\15\bin\psql.exe" --version
    echo.
    echo Pulando instalacao...
    echo.
    pause
    exit /b 0
)

REM Verificar permissoes de admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Precisa ser executado como Administrador!
    echo.
    echo Clique com botao direito neste arquivo e selecione:
    echo "Executar como administrador"
    echo.
    pause
    exit /b 1
)

echo [1/3] Conhecendo requisitos...
python --version
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    pause
    exit /b 1
)

echo.
echo [2/3] Baixando PostgreSQL (isso pode levar alguns minutos)...
set TEMP_DIR=%TEMP%\postgresql_setup
if not exist "!TEMP_DIR!" mkdir "!TEMP_DIR!"

set PG_FILE=%TEMP_DIR%\postgresql-15.7.exe
set PG_URL=https://get.enterprisedb.com/postgresql/postgresql-15.7-1-windows-x64.exe

REM Usar PowerShell para baixar
powershell -NoProfile -Command ^
    "$ProgressPreference='SilentlyContinue'; [Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PG_URL%' -OutFile '%PG_FILE%' -UseBasicParsing" 2>nul

if not exist "%PG_FILE%" (
    echo [ERRO] Nao conseguiu baixar PostgreSQL
    echo.
    echo Tente manualmente:
    echo https://www.postgresql.org/download/windows/
    echo.
    pause
    exit /b 1
)

echo [OK] Download concluido
echo.
echo [3/3] Instalando (isso pode levar alguns minutos)...
echo.

REM Executar instalador
"%PG_FILE%" --mode unattended --superpassword postgres123 --serverport 5432

REM Aguardar
timeout /t 10 /nobreak

REM Verificar
echo.
if exist "C:\Program Files\PostgreSQL\15\bin\psql.exe" (
    echo ======================================
    echo [OK] PostgreSQL instalado com sucesso!
    echo ======================================
    echo.
    "C:\Program Files\PostgreSQL\15\bin\psql.exe" --version
    echo.
    del "%PG_FILE%" 2>nul
    echo Instalacao concluida!
) else (
    echo [ERRO] Instalacao falhou
)

echo.
echo Pressione qualquer tecla para continuar...
pause >nul
