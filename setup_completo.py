#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script master para configurar tudo e deixar o servidor pronto
Executa em ordem:
  1. Instalar dependências Python
  2. Configurar MySQL
  3. Testar e exibir próximos passos
"""

import subprocess
import sys
import os

def print_header(texto):
    print("\n" + "="*70)
    print(f"  {texto}")
    print("="*70 + "\n")

def print_success(texto):
    print(f"✓ {texto}")

def print_error(texto):
    print(f"✗ {texto}")

def run_script(script_name, descricao):
    """Executa um script Python e aguarda conclusão"""
    print_header(descricao)
    
    if not os.path.exists(script_name):
        print_error(f"Arquivo {script_name} não encontrado")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False
        )
        
        if result.returncode != 0:
            print_error(f"Erro ao executar {script_name}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Erro: {e}")
        return False

def main():
    print_header("SETUP COMPLETO - SISTEMA DE ESTOQUE")
    
    print("Este script vai:")
    print("  1. Localizar/configurar MySQL")
    print("  2. Instalar todas as dependências Python")
    print("  3. Configurar o MySQL (banco + usuário)")
    print("  4. Atualizar arquivo .env")
    print("  5. Deixar servidor pronto\n")
    
    # Passo 0: Localizar MySQL
    if not run_script('encontrar_mysql.py', 'ETAPA 0/3: LOCALIZANDO MYSQL'):
        print("\n" + "!"*70)
        print("MySQL não foi encontrado. Por favor:")
        print("  1. Instale MySQL Community Server de: https://dev.mysql.com/downloads/mysql/")
        print("  2. Marque 'Add MySQL to PATH' durante a instalação")
        print("  3. Execute este script novamente")
        print("!"*70)
        return 1
    
    # Passo 1: Instalar dependências
    if not run_script('instalar_dependencias.py', 'ETAPA 1/3: INSTALANDO DEPENDÊNCIAS PYTHON'):
        print_error("Falha na instalação de dependências")
        return 1
    
    # Passo 2: Configurar MySQL
    if not run_script('configurar_mysql.py', 'ETAPA 2/3: CONFIGURANDO MYSQL'):
        print_error("Falha na configuração do MySQL")
        print("\nDica: Verifique se MySQL está instalado e rodando")
        return 1
    
    # Conclusão
    print_header("TUDO PRONTO! 🎉")
    
    print("✓ Dependências instaladas")
    print("✓ MySQL configurado")
    print("✓ Arquivo .env atualizado\n")
    
    print("Para iniciar o servidor Flask:")
    print("\n  python app.py\n")
    
    print("O servidor estará disponível em:")
    print("  http://localhost:5000\n")
    
    print("Login padrão:")
    print("  Usuário: admin")
    print("  Senha: admin\n")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nSetup cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erro: {e}")
        sys.exit(1)
