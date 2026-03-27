#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para instalar todas as dependências do projeto
"""

import subprocess
import sys
import os

def main():
    print("\n" + "="*70)
    print("  INSTALADOR DE DEPENDÊNCIAS - SISTEMA DE ESTOQUE")
    print("="*70 + "\n")
    
    # Mudar para diretório do projeto
    projeto_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(projeto_dir)
    
    print(f"Diretório: {projeto_dir}\n")
    
    # Verificar se requirements.txt existe
    if not os.path.exists('requirements.txt'):
        print("✗ Erro: requirements.txt não encontrado!")
        return 1
    
    # Instalar
    print("Instalando dependências...")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '--upgrade'],
            capture_output=False
        )
        
        if result.returncode != 0:
            print("\n✗ Erro ao instalar dependências")
            return 1
        
        print("\n" + "="*70)
        print("✓ DEPENDÊNCIAS INSTALADAS COM SUCESSO!")
        print("="*70 + "\n")
        
        # Verificar instalação
        print("Verificando pacotes instalados:")
        subprocess.run([sys.executable, '-m', 'pip', 'list'])
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
