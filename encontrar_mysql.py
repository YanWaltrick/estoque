#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar MySQL e adicionar ao PATH se necessário
"""

import subprocess
import sys
import os
from pathlib import Path

def find_mysql():
    """Procura por MySQL em localizações comuns"""
    mysql_paths = [
        r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe',
        r'C:\Program Files\MySQL\MySQL Server 8.1\bin\mysql.exe',
        r'C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe',
        r'C:\MySQL\bin\mysql.exe',
    ]
    
    print("\nProcurando MySQL nas localizações padrão...\n")
    
    for path in mysql_paths:
        if Path(path).exists():
            print(f"✓ MySQL encontrado em: {path}")
            return path
    
    print("✗ MySQL não foi encontrado nas localizações padrão")
    return None

def add_to_path(mysql_path):
    """Adiciona MySQL ao PATH do sistema"""
    bin_dir = os.path.dirname(mysql_path)
    
    # Adicionar ao PATH da sessão atual
    os.environ['PATH'] = bin_dir + os.pathsep + os.environ['PATH']
    
    print(f"✓ MySQL adicionado ao PATH da sessão: {bin_dir}")
    return bin_dir

def test_mysql():
    """Testa se mysql está acessível"""
    try:
        result = subprocess.run(
            ['mysql', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ Teste bem-sucedido: {result.stdout.strip()}")
            return True
    except Exception as e:
        print(f"✗ Erro ao testar MySQL: {e}")
    
    return False

def main():
    print("\n" + "="*70)
    print("  LOCALIZADOR DE MYSQL")
    print("="*70)
    
    # Tentar encontrar
    mysql_path = find_mysql()
    
    if not mysql_path:
        print("\n" + "!"*70)
        print("MySQL não foi encontrado no seu sistema!")
        print("\nPara instalar MySQL no Windows:")
        print("  1. Acesse: https://dev.mysql.com/downloads/mysql/")
        print("  2. Baixe MySQL Community Server (recomendo versão 8.0+)")
        print("  3. Execute o instalador")
        print("  4. IMPORTANTE: Marque 'Add MySQL to PATH'")
        print("  5. Conclua a instalação")
        print("  6. Reinicie este script")
        print("!"*70)
        return 1
    
    # Adicionar ao PATH
    add_to_path(mysql_path)
    
    # Testar
    print("\nTestando conexão...")
    if test_mysql():
        print("\n✓ MySQL está pronto para usar!")
        return 0
    else:
        print("\n✗ Não conseguiu conectar ao MySQL")
        print("Verifique se o serviço MySQL está rodando")
        return 1

if __name__ == '__main__':
    sys.exit(main())
