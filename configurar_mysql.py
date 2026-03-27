#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar MySQL automaticamente
Cria banco de dados, usuário e atualiza .env
"""

import subprocess
import sys
import os
import getpass
from pathlib import Path

def print_header(texto):
    print("\n" + "="*70)
    print(f"  {texto}")
    print("="*70)

def print_success(texto):
    print(f"✓ {texto}")

def print_error(texto):
    print(f"✗ {texto}")

def check_mysql_installed():
    """Verifica se MySQL está instalado"""
    try:
        result = subprocess.run(
            ['mysql', '--version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print_success(f"MySQL encontrado: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print_error("MySQL não encontrado no PATH")
    return False

def execute_mysql_command(sql, usuario='root', senha=''):
    """Executa comando SQL no MySQL"""
    try:
        if senha:
            # Usar -e para passar comando diretamente
            cmd = f"mysql -u {usuario} -p{senha} -h localhost -e \"{sql}\""
        else:
            cmd = f"mysql -u {usuario} -h localhost"
        
        # Usar shell=True para aceitar entrada interativa
        proc = subprocess.Popen(
            cmd,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = proc.communicate(input=sql + '\n')
        
        if proc.returncode != 0 and stderr:
            return False, stderr
        return True, stdout
        
    except Exception as e:
        return False, str(e)

def criar_banco_e_usuario(usuario='estoque_user', senha='12345', dbname='estoque_db'):
    """Cria banco de dados e usuário no MySQL"""
    print_header("CONFIGURANDO MYSQL - CRIANDO BANCO E USUÁRIO")
    
    print(f"\nParâmetros:")
    print(f"  Banco de dados: {dbname}")
    print(f"  Usuário: {usuario}")
    print(f"  Senha: {'*' * len(senha)}")
    print(f"  Host: localhost/remoto\n")
    
    # Solicitar senha do root
    senha_root = getpass.getpass("Digite a senha do usuário 'root' do MySQL: ")
    
    if not senha_root:
        print_error("Senha não foi digitada")
        return False
    
    # Criar comandos SQL
    sql_commands = [
        f"CREATE DATABASE IF NOT EXISTS {dbname} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        f"CREATE USER IF NOT EXISTS '{usuario}'@'%' IDENTIFIED BY '{senha}';",
        f"GRANT ALL PRIVILEGES ON {dbname}.* TO '{usuario}'@'%';",
        "FLUSH PRIVILEGES;",
    ]
    
    print(f"\nExecutando comandos SQL no MySQL...")
    
    for cmd in sql_commands:
        print(f"  → {cmd}")
        sucesso, msg = execute_mysql_command(cmd, 'root', senha_root)
        
        if not sucesso and 'already exists' not in str(msg):
            if msg and 'Access denied' in msg:
                print_error(f"Acesso negado. Verifique a senha do root.")
                return False
            elif msg and 'Can\'t connect' in msg:
                print_error(f"Não conseguiu conectar ao MySQL. Verifique se está rodando.")
                return False
    
    print_success(f"Banco '{dbname}' e usuário '{usuario}' configurados")
    return True

def atualizar_env(usuario='estoque_user', senha='12345', dbname='estoque_db', host='localhost'):
    """Atualiza arquivo .env com configuração MySQL"""
    print_header("ATUALIZANDO ARQUIVO .env")
    
    env_file = Path('.env')
    if not env_file.exists():
        print_error("Arquivo .env não encontrado")
        return False
    
    database_url = f"mysql+pymysql://{usuario}:{senha}@{host}:3306/{dbname}"
    
    # Ler arquivo
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except Exception as e:
        print_error(f"Erro ao ler .env: {e}")
        return False
    
    # Substituir DATABASE_URL
    linhas = conteudo.split('\n')
    novas_linhas = []
    found = False
    
    for linha in linhas:
        if linha.startswith('DATABASE_URL='):
            novas_linhas.append(f'DATABASE_URL={database_url}')
            found = True
        else:
            novas_linhas.append(linha)
    
    # Se não encontrou, adicionar no início
    if not found:
        novas_linhas.insert(0, f'DATABASE_URL={database_url}')
    
    # Salvar
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(novas_linhas))
    except Exception as e:
        print_error(f"Erro ao salvar .env: {e}")
        return False
    
    print_success(f"Arquivo .env atualizado com:")
    print(f"  DATABASE_URL={database_url}\n")
    return True

def testar_conexao(usuario='estoque_user', senha='12345', dbname='estoque_db'):
    """Testa a conexão com o banco de dados"""
    print_header("TESTANDO CONEXÃO COM MYSQL")
    
    print(f"\nTestando: {usuario}@localhost:{dbname}")
    
    sql = "SELECT 1 as teste;"
    sucesso, msg = execute_mysql_command(sql, usuario, senha)
    
    if sucesso:
        print_success("Conexão bem-sucedida!")
        return True
    else:
        print_error(f"Erro na conexão: {msg}")
        return False

def main():
    print_header("CONFIGURADOR MYSQL - SISTEMA DE ESTOQUE")
    
    # Verificar MySQL
    if not check_mysql_installed():
        print("\n" + "!"*70)
        print("MySQL não foi encontrado no seu sistema.")
        print("\nPara instalar MySQL no Windows:")
        print("  1. Acesse: https://dev.mysql.com/downloads/mysql/")
        print("  2. Baixe a versão Community Server (recomendo 8.x)")
        print("  3. Execute o instalador")
        print("  4. Marque 'Add MySQL to PATH'")
        print("  5. Execute este script novamente")
        print("!"*70)
        return 1
    
    # Configurar
    usuario = 'estoque_user'
    senha = '12345'
    dbname = 'estoque_db'
    
    # Criar banco
    if not criar_banco_e_usuario(usuario, senha, dbname):
        return 1
    
    # Atualizar .env
    if not atualizar_env(usuario, senha, dbname, 'localhost'):
        return 1
    
    # Testar
    if not testar_conexao(usuario, senha, dbname):
        print("\n⚠ Aviso: A conexão falhou, mas .env foi atualizado")
        print("Você pode ajustar os parâmetros em .env manualmente se necessário")
    
    # Resumo
    print_header("CONFIGURAÇÃO CONCLUÍDA!")
    
    print("\n✓ Banco de dados configurado")
    print("✓ Usuário criado")
    print("✓ Arquivo .env atualizado\n")
    
    print("Próximos passos:")
    print("  1. Instale as dependências Python:")
    print("     python instalar_dependencias.py")
    print("\n  2. Inicie o servidor:")
    print("     python app.py")
    print("\n  3. Acesse no navegador:")
    print("     http://localhost:5000")
    print("\n  4. Login padrão:")
    print("     Usuário: admin")
    print("     Senha: admin\n")
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erro inesperado: {e}")
        sys.exit(1)
