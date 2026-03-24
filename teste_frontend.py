#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para verificar se o Frontend Web está funcionando corretamente
"""

import sys
import os

def testar_imports():
    """Testa se todas as dependências podem ser importadas"""
    print("\n" + "="*70)
    print("TESTANDO IMPORTAÇÕES".center(70))
    print("="*70 + "\n")
    
    testes = [
        ("json", "json"),
        ("os", "os"),
        ("datetime", "datetime"),
        ("Flask", "flask"),
        ("Werkzeug", "werkzeug"),
        ("estoque", "estoque"),
    ]
    
    falhas = []
    
    for nome, modulo in testes:
        try:
            __import__(modulo)
            print(f"✓ {nome:20} OK")
        except ImportError as e:
            print(f"✗ {nome:20} ERRO")
            falhas.append((nome, str(e)))
    
    return falhas


def testar_arquivos():
    """Testa se todos os arquivos necessários existem"""
    print("\n" + "="*70)
    print("VERIFICANDO ARQUIVOS".center(70))
    print("="*70 + "\n")
    
    arquivos_necessarios = [
        "estoque.py",
        "app.py",
        "requirements.txt",
        "templates/index.html",
        "static/css/style.css",
        "static/js/app.js",
    ]
    
    falhas = []
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"✓ {arquivo:35} ({tamanho:,} bytes)")
        else:
            print(f"✗ {arquivo:35} NÃO ENCONTRADO")
            falhas.append(arquivo)
    
    return falhas


def testar_classes():
    """Testa se as classes Python estão funcionando"""
    print("\n" + "="*70)
    print("TESTANDO CLASSES".center(70))
    print("="*70 + "\n")
    
    try:
        from estoque import Produto, Estoque
        
        # Testar classe Produto
        print("Testando classe Produto...")
        prod = Produto("TEST001", "Produto Teste", "Categoria Teste", 
                      100.00, 10, 5, "Localizacao Teste")
        
        assert prod.id_produto == "TEST001"
        assert prod.nome == "Produto Teste"
        assert prod.valor_total() == 1000.00
        assert prod.abaixo_minimo() == False
        print("✓ Classe Produto funcionando corretamente")
        
        # Testar classe Estoque
        print("Testando classe Estoque...")
        estoque = Estoque("teste_estoque.json")
        assert isinstance(estoque.produtos, dict)
        print("✓ Classe Estoque funcionando corretamente")
        
        return []
        
    except Exception as e:
        print(f"✗ Erro ao testar classes: {e}")
        return [str(e)]


def testar_api():
    """Testa se a API Flask pode ser importada"""
    print("\n" + "="*70)
    print("TESTANDO API FLASK".center(70))
    print("="*70 + "\n")
    
    try:
        from app import app, estoque
        print("✓ Módulo app.py importado com sucesso")
        print(f"✓ Aplicação Flask criada: {app.name}")
        print(f"✓ Instância Estoque: {type(estoque)}")
        
        # Listar rotas
        print("\nRotas disponíveis:")
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                metodos = ','.join(rule.methods - {'OPTIONS', 'HEAD'})
                print(f"  {rule.rule:40} [{metodos}]")
        
        return []
        
    except Exception as e:
        print(f"✗ Erro ao testar API: {e}")
        return [str(e)]


def main():
    """Função principal"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + "TESTE DO FRONTEND WEB - SISTEMA DE ESTOQUE".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    falhas_totais = []
    
    # Testar imports
    falhas = testar_imports()
    falhas_totais.extend(falhas)
    
    # Testar arquivos
    falhas = testar_arquivos()
    falhas_totais.extend(falhas)
    
    # Testar classes
    falhas = testar_classes()
    falhas_totais.extend(falhas)
    
    # Testar API
    falhas = testar_api()
    falhas_totais.extend(falhas)
    
    # Resultado final
    print("\n" + "="*70)
    
    if not falhas_totais:
        print("✓ TODOS OS TESTES PASSARAM COM SUCESSO!".center(70))
        print("="*70)
        print("\nO Frontend Web está pronto para usar.")
        print("Execute: python app.py")
        print("Acesse: http://localhost:5000")
        return 0
    else:
        print("✗ ALGUNS TESTES FALHARAM".center(70))
        print("="*70)
        print("\nProblemas encontrados:")
        for i, falha in enumerate(falhas_totais, 1):
            print(f"  {i}. {falha}")
        print("\nPara resolver:")
        print("  1. Instale as dependências: pip install -r requirements.txt")
        print("  2. Verifique se todos os arquivos estão no lugar correto")
        print("  3. Verifique a estrutura de diretórios")
        return 1
    
    print()


if __name__ == "__main__":
    sys.exit(main())
