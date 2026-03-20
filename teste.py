"""
Script de teste e demonstração do sistema de estoque
Executa operações automaticamente para testar funcionalidades
"""

from estoque import Estoque

def teste_sistema():
    """Executa uma série de testes no sistema"""
    
    print("="*70)
    print("TESTE AUTOMÁTICO DO SISTEMA DE ESTOQUE".center(70))
    print("="*70)
    
    # Criar instância do estoque
    estoque = Estoque("teste_estoque.json")
    
    print("\n[TEST 1] Adicionando produtos de teste...\n")
    
    produtos_teste = [
        ("TEST001", "Camiseta Azul", "Vestuário", 59.90, 50, 10, "Prateleira 1"),
        ("TEST002", "Calça Jeans", "Vestuário", 129.90, 30, 5, "Prateleira 2"),
        ("TEST003", "Tênis Esportivo", "Calçados", 199.90, 20, 8, "Prateleira 3"),
        ("TEST004", "Boné", "Acessórios", 49.90, 100, 20, "Prateleira 4"),
        ("TEST005", "Mochila", "Acessórios", 89.90, 15, 5, "Prateleira 5"),
    ]
    
    for id_prod, nome, categoria, preco, qtd, minimo, local in produtos_teste:
        estoque.adicionar_produto(id_prod, nome, categoria, preco, qtd, minimo, local)
    
    print("\n[TEST 2] Listando todos os produtos...\n")
    estoque.listar_produtos()
    
    print("[TEST 3] Buscando um produto específico (TEST001)...\n")
    prod = estoque.buscar_produto("TEST001")
    if prod:
        print(f"Encontrado: {prod.nome}")
        print(f"Preço: R${prod.preco:.2f}")
        print(f"Quantidade: {prod.quantidade} unidades\n")
    
    print("[TEST 4] Registrando entrada de estoque (compra)...\n")
    estoque.entrada_estoque("TEST002", 20)
    print(f"Calça Jeans agora tem: {estoque.produtos['TEST002'].quantidade} unidades\n")
    
    print("[TEST 5] Registrando saída de estoque (venda)...\n")
    estoque.saida_estoque("TEST003", 5)
    print(f"Tênis Esportivo agora tem: {estoque.produtos['TEST003'].quantidade} unidades\n")
    
    print("[TEST 6] Tentando venda com quantidade insuficiente...\n")
    estoque.saida_estoque("TEST001", 200)  # Vai falhar
    print()
    
    print("[TEST 7] Verificando produtos abaixo do mínimo...\n")
    estoque.relatorio_minimo()
    
    print("[TEST 8] Relatório de valor total do estoque...\n")
    estoque.relatorio_valor_total()
    
    print("[TEST 9] Relatório por categoria...\n")
    estoque.relatorio_por_categoria()
    
    print("[TEST 10] Atualizando quantidade manualmente...\n")
    estoque.atualizar_quantidade("TEST004", 50)
    print(f"Boné agora tem: {estoque.produtos['TEST004'].quantidade} unidades\n")
    
    print("[TEST 11] Removendo um produto...\n")
    estoque.remover_produto("TEST005")
    print()
    
    print("[TEST 12] Listando produtos finais...\n")
    estoque.listar_produtos()
    
    print("="*70)
    print("TESTES CONCLUÍDOS COM SUCESSO! ✓".center(70))
    print("="*70)
    print("\nArquivo de teste criado: teste_estoque.json")
    print("Você pode reexecutar este script ou usar o menu interativo.\n")

if __name__ == "__main__":
    teste_sistema()
