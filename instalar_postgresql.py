#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador PostgreSQL para Sistema de Estoque
Requer privilégios de administrador
"""

import os
import sys
import subprocess
import ctypes
import urllib.request
import time
from pathlib import Path

def is_admin():
    """Verifica se está rodando como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def request_admin():
    """Solicita privilégios de administrador"""
    if not is_admin():
        print("Solicitando privilégios de administrador...")
        # Reexecuta com admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def check_postgresql():
    """Verifica se PostgreSQL já está instalado"""
    pg_path = Path("C:\\Program Files\\PostgreSQL\\15\\bin\\psql.exe")
    return pg_path.exists()

def download_postgresql():
    """Baixa instalador PostgreSQL"""
    url = "https://get.enterprisedb.com/postgresql/postgresql-15.7-1-windows-x64.exe"
    temp_dir = Path(os.environ['TEMP']) / 'postgresql_setup'
    temp_dir.mkdir(exist_ok=True)
    
    output_file = temp_dir / 'postgresql-15.7.exe'
    
    if output_file.exists():
        print(f"[OK] Arquivo já baixado: {output_file}")
        return output_file
    
    print(f"Baixando PostgreSQL de: {url}")
    print("Isso pode levar alguns minutos...")
    
    try:
        urllib.request.urlretrieve(url, str(output_file), reporthook)
        if output_file.exists():
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"\n[OK] Download concluido: {size_mb:.2f} MB")
            return output_file
        else:
            print("[ERRO] Falha ao baixar arquivo")
            return None
    except Exception as e:
        print(f"[ERRO] Erro ao baixar: {e}")
        return None

def reporthook(blocknum, blocksize, totalsize):
    """Mostra progresso do download"""
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = min(readsofar * 100.0 / totalsize, 100.0)
        s = f"\r[{percent:5.1f}%] {readsofar} / {totalsize} bytes"
        sys.stderr.write(s)
        if readsofar >= totalsize:
            sys.stderr.write("\n")

def install_postgresql(installer_path):
    """Executa instalador PostgreSQL"""
    print("\nInstalando PostgreSQL...")
    print("Isso pode levar vários minutos. Por favor, aguarde...")
    
    try:
        # Parâmetros de instalação silenciosa
        args = [
            str(installer_path),
            "--mode", "unattended",
            "--superpassword", "postgres123",
            "--serverport", "5432",
            "--locale", "pt_BR",
            "--components", "server,pgAdmin",
            "--disable-components", "stackbuilder"
        ]
        
        # Executar instalador
        result = subprocess.run(args, capture_output=True, text=True)
        
        # Aguardar conclusão
        time.sleep(15)
        
        return check_postgresql()
    except Exception as e:
        print(f"[ERRO] Erro ao executar instalador: {e}")
        return False

def verify_installation():
    """Verifica se instalação foi bem-sucedida"""
    pg_path = Path("C:\\Program Files\\PostgreSQL\\15\\bin\\psql.exe")
    
    if pg_path.exists():
        try:
            result = subprocess.run([str(pg_path), "--version"], capture_output=True, text=True)
            print(f"\n[OK] {result.stdout.strip()}")
            return True
        except:
            return False
    return False

def main():
    """Função principal"""
    print("")
    print("=" * 50)
    print("PostgreSQL Installer - Sistema de Estoque")
    print("=" * 50)
    print("")
    
    # Solicitar admin
    request_admin()
    
    # Verificar se já está instalado
    if check_postgresql():
        print("[OK] PostgreSQL já está instalado!")
        verify_installation()
        print("\nPulando instalação...")
        return 0
    
    # Baixar
    print("[1/3] Baixando PostgreSQL...")
    installer = download_postgresql()
    
    if not installer:
        print("\n[ERRO] Não conseguiu baixar PostgreSQL")
        print("\nTente manualmente:")
        print("https://www.postgresql.org/download/windows/")
        return 1
    
    # Instalar
    print("\n[2/3] Instalando PostgreSQL...")
    if not install_postgresql(installer):
        print("\n[ERRO] Falha durante instalação")
        return 1
    
    # Verificar
    print("\n[3/3] Verificando instalação...")
    if verify_installation():
        print("")
        print("=" * 50)
        print("[OK] PostgreSQL INSTALADO COM SUCESSO!")
        print("=" * 50)
        print("")
        print("Próximos passos:")
        print("1. Feche esta janela")
        print("2. Execute: python app.py")
        print("3. Acesse: http://localhost:5000")
        print("")
        
        # Limpar arquivo
        try:
            installer.unlink()
        except:
            pass
        
        return 0
    else:
        print("\n[ERRO] PostgreSQL não foi encontrado após instalação")
        print("\nTente manualmente:")
        print("https://www.postgresql.org/download/windows/")
        return 1

if __name__ == '__main__':
    sys.exit(main())
