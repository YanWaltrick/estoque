#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para configurar PostgreSQL e criar banco de dados automaticamente
Execução: python setup_postgres.py
"""

import subprocess
import sys
import getpass
import os
from pathlib import Path

def print_header(texto):
    print("\n" + "="*70)
    print(f"  {texto}")
    print("="*70 + "\n")

def print_success(texto):
    print(f"✓ {texto}")

def print_error(texto):
    print(f"✗ {texto}")

def check_postgresql_installed():
    """Verifica se PostgreSQL está instalado"""
    try:
        resultado = subprocess.run(
            ['psql', '--version'],
            capture_output=True,
            text=True
        )
        if resultado.returncode == 0:
            print_success(f"PostgreSQL encontrado: {resultado.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print_error("PostgreSQL não encontrado no PATH")
    return False

def executar_comando_psql(comando, usuario='postgres', senha=''):
    """Executa comando no PostgreSQL"""
    try:
        # Preparar comando com PGPASSWORD
        env = os.environ.copy()
        if senha:
            env['PGPASSWORD'] = senha
        
        # Executar psql
        proc = subprocess.Popen(
            ['psql', '-U', usuario, '-h', 'localhost'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        stdout, stderr = proc.communicate(input=comando)
        
        if proc.returncode != 0:
            return False, stderr
        return True, stdout
        
    except Exception as e:
        return False, str(e)

def criar_usuario_postgres(username='estoque_user', password='12345'):
    """Cria usuário no PostgreSQL"""
    print_header("CRIANDO USUÁRIO NO POSTGRESQL")
    
    print("Você será solicitado a digitar a senha do usuário 'postgres'")
    print("(Senha definida durante a instalação do PostgreSQL)\n")
    
    senha_postgres = getpass.getpass("Senha do PostgreSQL (usuário 'postgres'): ")
    
    # Comando SQL para criar usuário
    comando_sql = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_user WHERE usename = '{username}') THEN
            CREATE USER {username} WITH PASSWORD '{password}';
            RAISE NOTICE 'Usuário {username} criado com sucesso';
        ELSE
            RAISE NOTICE 'Usuário {username} já existe';
        END IF;
    END $$;
    """
    
    sucesso, mensagem = executar_comando_psql(comando_sql, 'postgres', senha_postgres)
    
    if sucesso:
        print_success(f"Usuário '{username}' configurado")
        return True
    else:
        print_error(f"Erro ao criar usuário: {mensagem}")
        return False

def criar_banco_dados(dbname='estoque_db', username='estoque_user', password='12345'):
    """Cria banco de dados no PostgreSQL"""
    print_header("CRIANDO BANCO DE DADOS")
    
    print(f"Criando banco de dados: {dbname}")
    print(f"Proprietário: {username}\n")
    
    # Comando SQL para criar banco
    comando_sql = f"""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '{dbname}') THEN
            CREATE DATABASE {dbname} OWNER {username};
            RAISE NOTICE 'Banco {dbname} criado com sucesso';
        ELSE
            RAISE NOTICE 'Banco {dbname} já existe';
        END IF;
    END $$;
    """
    
    # Precisa da senha do postgres
    print("Digite a senha do PostgreSQL (usuário 'postgres'):")
    senha_postgres = getpass.getpass("Senha: ")
    
    sucesso, mensagem = executar_comando_psql(comando_sql, 'postgres', senha_postgres)
    
    if sucesso:
        print_success(f"Banco de dados '{dbname}' configurado")
        # Conceder privilégios
        comando_privilegios = f"GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {username};"
        executar_comando_psql(comando_privilegios, 'postgres', senha_postgres)
        print_success(f"Privilégios concedidos a '{username}'")
        return True
    else:
        print_error(f"Erro ao criar banco: {mensagem}")
        return False

def atualizar_env(tipo='localhost', ip='localhost', username='estoque_user', password='12345'):
    """Atualiza arquivo .env com configurações"""
    print_header("ATUALIZANDO ARQUIVO .env")
    
    env_file = Path('.env')
    if not env_file.exists():
        print_error("Arquivo .env não encontrado na pasta atual")
        return False
    
    # Preparar nova DATABASE_URL
    if tipo == 'remoto':
        database_url = f"postgresql://{username}:{password}@{ip}:5432/estoque_db"
    else:
        database_url = f"postgresql://{username}:{password}@localhost:5432/estoque_db"
    
    # Ler arquivo
    with open(env_file, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    # Atualizar DATABASE_URL (encontrar a linha e substituir)
    if 'DATABASE_URL=postgresql://' in conteudo:
        # Substituir linha existente
        linhas = conteudo.split('\n')
        newlinhas = []
        for linha in linhas:
            if linha.startswith('DATABASE_URL=postgresql://'):
                newlinhas.append(f"DATABASE_URL={database_url}")
            else:
                newlinhas.append(linha)
        conteudo = '\n'.join(newlinhas)
    
    # Salvar arquivo
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    
    print_success(f"Arquivo .env atualizado")
    print(f"DATABASE_URL={database_url}")
    return True

def menu_principal():
    """Menu principal de configuração"""
    print_header("CONFIGURADOR POSTGRESQL - SISTEMA DE ESTOQUE")
    
    print("\nOpções disponíveis:")
    print("1) Instalação completa (criar usuário + banco + atualizar .env)")
    print("2) Apenas criar usuário PostgreSQL")
    print("3) Apenas criar banco de dados")
    print("4) Apenas atualizar arquivo .env")
    print("0) Sair\n")
    
    opcao = input("Escolha uma opção (0-4): ").strip()
    
    if opcao == '1':
        # Instalação completa
        username = input("\nNome de usuário PostgreSQL [estoque_user]: ").strip() or 'estoque_user'
        password = input("Senha do usuário [12345]: ").strip() or '12345'
        
        if criar_usuario_postgres(username, password):
            if criar_banco_dados('estoque_db', username, password):
                if atualizar_env('localhost', 'localhost', username, password):
                    print_header("CONFIGURAÇÃO CONCLUÍDA!")
                    print("\nPróximos passos:")
                    print("1) Instale as dependências Python:")
                    print("   pip install -r requirements.txt")
                    print("\n2) Execute a aplicação:")
                    print("   python app.py")
                    print("\n3) Acesse em seu navegador:")
                    print("   http://localhost:5000")
                    print("\n4) Faça login com:")
                    print("   Usuário: admin")
                    print("   Senha: admin")
    
    elif opcao == '2':
        username = input("\nNome de usuário PostgreSQL [estoque_user]: ").strip() or 'estoque_user'
        password = input("Senha do usuário [12345]: ").strip() or '12345'
        criar_usuario_postgres(username, password)
    
    elif opcao == '3':
        username = input("\nNome de usuário PostgreSQL [estoque_user]: ").strip() or 'estoque_user'
        password = input("Senha do usuário [12345]: ").strip() or '12345'
        criar_banco_dados('estoque_db', username, password)
    
    elif opcao == '4':
        print("\nConfiguração do banco:")
        tipo = input("Servidor local ou remoto? [local/remoto] ").strip().lower() or 'local'
        username = input("Usuário PostgreSQL [estoque_user]: ").strip() or 'estoque_user'
        password = input("Senha [12345]: ").strip() or '12345'
        
        if tipo == 'remoto':
            ip = input("IP do servidor PostgreSQL: ").strip()
            atualizar_env('remoto', ip, username, password)
        else:
            atualizar_env('localhost', 'localhost', username, password)
    
    elif opcao == '0':
        print("\nSaindo...")
        sys.exit(0)
    else:
        print_error("Opção inválida!")

def main():
    """Função principal"""
    try:
        # Verificar se PostgreSQL está instalado
        if not check_postgresql_installed():
            print_error("\nPostgreSQL não está instalado ou não está no PATH.")
            print("\nPara instalar:")
            print("  Windows: https://www.postgresql.org/download/windows/")
            print("\nDepois de instalar, adicione PostgreSQL ao PATH ou use psql com caminho completo.")
            sys.exit(1)
        
        # Mostrar menu
        menu_principal()
        
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print_error(f"\nErro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
