# Script para instalar PostgreSQL automaticamente
# Versao: PostgreSQL 15.x

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Instalador PostgreSQL - Sistema Estoque" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se PostgreSQL ja esta instalado
$pgPath = "C:\Program Files\PostgreSQL\15\bin\psql.exe"
if (Test-Path $pgPath) {
    Write-Host "[OK] PostgreSQL ja esta instalado" -ForegroundColor Green
    & $pgPath --version
    Write-Host ""
    Write-Host "Pulando instalacao..." -ForegroundColor Yellow
    exit 0
}

# URL do instalador PostgreSQL 15
$downloadUrl = "https://get.enterprisedb.com/postgresql/postgresql-15.7-1-windows-x64.exe"
$installerPath = "$env:TEMP\postgresql-installer.exe"

Write-Host "Etapa 1: Baixando PostgreSQL..." -ForegroundColor Yellow
Write-Host "URL: $downloadUrl" -ForegroundColor Gray

try {
    # Usar Net.ServicePointManager para melhorar compatibilidade
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    
    # Mostrar progresso
    $progressPreference = 'SilentlyContinue'
    
    Invoke-WebRequest -Uri $downloadUrl -OutFile $installerPath -UseBasicParsing -TimeoutSec 300
    
    if (Test-Path $installerPath) {
        $size = (Get-Item $installerPath).Length / 1MB
        Write-Host "[OK] Download concluido: $([Math]::Round($size, 2)) MB" -ForegroundColor Green
    } else {
        throw "Arquivo nao foi salvo"
    }
} catch {
    Write-Host "[ERRO] Falha ao baixar: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternativa: Baixe manualmente de:" -ForegroundColor Yellow
    Write-Host "https://www.postgresql.org/download/windows/" -ForegroundColor Cyan
    exit 1
}

Write-Host ""
Write-Host "Etapa 2: Instalando PostgreSQL..." -ForegroundColor Yellow
Write-Host "Isso pode levar alguns minutos..." -ForegroundColor Gray

# Parametros de instalacao silenciosa
$instParams = @(
    "--mode", "unattended",
    "--superpassword", "postgres123",
    "--serverport", "5432",
    "--locale", "pt_BR",
    "--components", "server,pgAdmin"
)

try {
    # Executar instalador
    & $installerPath @instParams
    $exitCode = $LASTEXITCODE
    
    if ($exitCode -eq 0) {
        Write-Host "[OK] PostgreSQL instalado com sucesso!" -ForegroundColor Green
    } else {
        Write-Host "[AVISO] Instalador retornou codigo: $exitCode" -ForegroundColor Yellow
        Write-Host "Verificando se PostgreSQL foi instalado..." -ForegroundColor Gray
    }
} catch {
    Write-Host "[AVISO] Erro durante instalacao: $_" -ForegroundColor Yellow
}

# Verificar se foi instalado
Start-Sleep -Seconds 5
if (Test-Path $pgPath) {
    Write-Host "[OK] PostgreSQL foi instalado com sucesso!" -ForegroundColor Green
    & $pgPath --version
} else {
    Write-Host "[ERRO] PostgreSQL nao foi encontrado apos instalacao" -ForegroundColor Red
    exit 1
}

# Limpar arquivo temporario
Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Etapa 3: Configure o banco de dados..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Pressione ENTER para continuar com a configuracao..." -ForegroundColor Cyan
Read-Host

exit 0
