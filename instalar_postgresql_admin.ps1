# Requer privilégios de administrador
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Solicitando privilégios de administrador..." -ForegroundColor Yellow
    $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    Start-Process powershell -Verb RunAs -ArgumentList $arguments
    exit
}

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Instalador PostgreSQL - Sistema Estoque" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se já está instalado
$pgPath = "C:\Program Files\PostgreSQL\15\bin\psql.exe"
if (Test-Path $pgPath) {
    Write-Host "[OK] PostgreSQL ja esta instalado!" -ForegroundColor Green
    & $pgPath --version
    Write-Host ""
    Write-Host "Pulando instalacao..." -ForegroundColor Yellow
    Read-Host "Pressione ENTER para sair"
    exit 0
}

Write-Host "[1/4] Verificando requisitos..." -ForegroundColor Yellow

# Verificar Python
python --version 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERRO] Python nao encontrado!" -ForegroundColor Red
    Read-Host "Pressione ENTER para sair"
    exit 1
}

Write-Host "[OK] Python encontrado" -ForegroundColor Green
Write-Host ""

# Criar diretório temporário
$tempDir = "$env:TEMP\postgresql_setup"
if (-not (Test-Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
}

$pgFile = "$tempDir\postgresql-15.7.exe"
$pgUrl = "https://get.enterprisedb.com/postgresql/postgresql-15.7-1-windows-x64.exe"

Write-Host "[2/4] Baixando PostgreSQL (361 MB)..." -ForegroundColor Yellow
Write-Host "Isso pode levar alguns minutos..." -ForegroundColor Gray

try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $progressPreference = 'SilentlyContinue'
    
    Invoke-WebRequest -Uri $pgUrl -OutFile $pgFile -UseBasicParsing -TimeoutSec 300
    
    if (Test-Path $pgFile) {
        $size = [Math]::Round((Get-Item $pgFile).Length / 1MB, 2)
        Write-Host "[OK] Download concluido: $size MB" -ForegroundColor Green
    } else {
        throw "Arquivo nao foi baixado"
    }
} catch {
    Write-Host "[ERRO] Falha ao baixar: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Tente manualmente de:" -ForegroundColor Yellow
    Write-Host "https://www.postgresql.org/download/windows/" -ForegroundColor Cyan
    Read-Host "Pressione ENTER para sair"
    exit 1
}

Write-Host ""
Write-Host "[3/4] Instalando PostgreSQL..." -ForegroundColor Yellow
Write-Host "Porfavor aguarde (pode levar varios minutos)..." -ForegroundColor Gray

try {
    & $pgFile --mode unattained --superpassword postgres123 --serverport 5432 --locale pt_BR --components server,pgAdmin --disable-components stackbuilder
    
    # Aguardar conclusão
    Start-Sleep -Seconds 15
} catch {
    Write-Host "[AVISO] Instalador teve problema: $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[4/4] Verificando instalacao..." -ForegroundColor Yellow

if (Test-Path $pgPath) {
    Write-Host ""
    Write-Host "======================================" -ForegroundColor Green
    Write-Host "[OK] PostgreSQL instalado com sucesso!" -ForegroundColor Green
    Write-Host "======================================" -ForegroundColor Green
    Write-Host ""
    
    & $pgPath --version
    
    Write-Host ""
    Write-Host "Limpando arquivos temporarios..." -ForegroundColor Gray
    Remove-Item $pgFile -Force -ErrorAction SilentlyContinue
    
    Write-Host "[OK] Limpeza concluida" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[ERRO] PostgreSQL nao foi encontrado apos instalacao" -ForegroundColor Red
    Write-Host ""
    Write-Host "Tente manualmente:" -ForegroundColor Yellow
    Write-Host "1. Baixe de: https://www.postgresql.org/download/windows/" -ForegroundColor Cyan
    Write-Host "2. Execute o instalador" -ForegroundColor Cyan
    Write-Host "3. Anote a senha do usuario 'postgres'" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Pressione ENTER para continuar..." -ForegroundColor Cyan
Read-Host
