import json
import os
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional


def now_gmt3():
    return datetime.now(timezone(timedelta(hours=-3)))

class Produto:
    """Classe para representar um produto do estoque"""
    
    def __init__(self, id_produto: str, nome: str, categoria: str, preco: float, 
                 quantidade: int, minimo: int, localizacao: str = ""):
        self.id_produto = id_produto
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.quantidade = quantidade
        self.minimo = minimo
        self.localizacao = localizacao
        self.data_criacao = now_gmt3().strftime("%d/%m/%Y %H:%M:%S")
    
    def to_dict(self) -> dict:
        """Converte o produto para dicionário"""
        return {
            "id_produto": self.id_produto,
            "nome": self.nome,
            "categoria": self.categoria,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "minimo": self.minimo,
            "localizacao": self.localizacao,
            "data_criacao": self.data_criacao
        }
    
    @staticmethod
    def from_dict(dados: dict) -> 'Produto':
        """Cria um produto a partir de um dicionário"""
        produto = Produto(
            dados["id_produto"],
            dados["nome"],
            dados["categoria"],
            dados["preco"],
            dados["quantidade"],
            dados["minimo"],
            dados.get("localizacao", "")
        )
        produto.data_criacao = dados.get("data_criacao", produto.data_criacao)
        return produto
    
    def valor_total(self) -> float:
        """Calcula o valor total do produto em estoque"""
        return self.quantidade * self.preco
    
    def abaixo_minimo(self) -> bool:
        """Verifica se o produto está abaixo do estoque mínimo"""
        return self.quantidade < self.minimo


class Estoque:
    """Classe para gerenciar o estoque da empresa"""
    
    def __init__(self, arquivo_dados: str = "dados_estoque.json"):
        self.arquivo_dados = arquivo_dados
        self.produtos: Dict[str, Produto] = {}
        self.carregar_dados()
    
    def carregar_dados(self) -> None:
        """Carrega os dados do arquivo JSON"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    for id_prod, prod_dict in dados.items():
                        self.produtos[id_prod] = Produto.from_dict(prod_dict)
                print(f"✓ Dados carregados: {len(self.produtos)} produtos")
            except Exception as e:
                print(f"✗ Erro ao carregar dados: {e}")
        else:
            print("Iniciando novo estoque...")
    
    def salvar_dados(self) -> None:
        """Salva os dados no arquivo JSON"""
        try:
            dados = {id_prod: prod.to_dict() 
                    for id_prod, prod in self.produtos.items()}
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"✗ Erro ao salvar dados: {e}")
    
    def adicionar_produto(self, id_produto: str, nome: str, categoria: str, 
                         preco: float, quantidade: int, minimo: int, 
                         localizacao: str = "") -> bool:
        """Adiciona um novo produto ao estoque"""
        if id_produto in self.produtos:
            print(f"✗ Produto com ID '{id_produto}' já existe!")
            return False
        
        if preco <= 0 or quantidade < 0:
            print("✗ Preço e quantidade devem ser positivos!")
            return False
        
        self.produtos[id_produto] = Produto(id_produto, nome, categoria, preco, 
                                           quantidade, minimo, localizacao)
        self.salvar_dados()
        print(f"✓ Produto '{nome}' adicionado com sucesso!")
        return True
    
    def remover_produto(self, id_produto: str) -> bool:
        """Remove um produto do estoque"""
        if id_produto not in self.produtos:
            print(f"✗ Produto com ID '{id_produto}' não encontrado!")
            return False
        
        nome = self.produtos[id_produto].nome
        del self.produtos[id_produto]
        self.salvar_dados()
        print(f"✓ Produto '{nome}' removido com sucesso!")
        return True
    
    def atualizar_quantidade(self, id_produto: str, nova_quantidade: int) -> bool:
        """Atualiza a quantidade de um produto"""
        if id_produto not in self.produtos:
            print(f"✗ Produto com ID '{id_produto}' não encontrado!")
            return False
        
        if nova_quantidade < 0:
            print("✗ Quantidade não pode ser negativa!")
            return False
        
        self.produtos[id_produto].quantidade = nova_quantidade
        self.salvar_dados()
        print(f"✓ Quantidade atualizada para {nova_quantidade} unidades!")
        return True
    
    def entrada_estoque(self, id_produto: str, quantidade: int) -> bool:
        """Registra entrada de produtos no estoque"""
        if id_produto not in self.produtos:
            print(f"✗ Produto com ID '{id_produto}' não encontrado!")
            return False
        
        if quantidade <= 0:
            print("✗ Quantidade deve ser maior que zero!")
            return False
        
        self.produtos[id_produto].quantidade += quantidade
        self.salvar_dados()
        print(f"✓ {quantidade} unidades adicionadas ao estoque!")
        return True
    
    def saida_estoque(self, id_produto: str, quantidade: int) -> bool:
        """Registra saída de produtos do estoque"""
        if id_produto not in self.produtos:
            print(f"✗ Produto com ID '{id_produto}' não encontrado!")
            return False
        
        if quantidade <= 0:
            print("✗ Quantidade deve ser maior que zero!")
            return False
        
        if self.produtos[id_produto].quantidade < quantidade:
            print(f"✗ Quantidade insuficiente! Disponível: {self.produtos[id_produto].quantidade}")
            return False
        
        self.produtos[id_produto].quantidade -= quantidade
        self.salvar_dados()
        print(f"✓ {quantidade} unidades removidas do estoque!")
        return True
    
    def buscar_produto(self, id_produto: str) -> Optional[Produto]:
        """Busca um produto pelo ID"""
        return self.produtos.get(id_produto)
    
    def listar_produtos(self) -> None:
        """Lista todos os produtos do estoque"""
        if not self.produtos:
            print("\n✗ Estoque vazio!\n")
            return
        
        print("\n" + "="*100)
        print(f"{'ID':<12} | {'Nome':<20} | {'Categoria':<15} | {'Preço':<10} | {'Qtd':<6} | {'Valor Total':<12} | {'Status':<10}")
        print("="*100)
        
        for prod in self.produtos.values():
            status = "BAIXO" if prod.abaixo_minimo() else "OK"
            print(f"{prod.id_produto:<12} | {prod.nome:<20} | {prod.categoria:<15} | "
                  f"R${prod.preco:<9.2f} | {prod.quantidade:<6} | R${prod.valor_total():<11.2f} | {status:<10}")
        
        print("="*100 + "\n")
    
    def produtos_abaixo_minimo(self) -> List[Produto]:
        """Retorna produtos abaixo do estoque mínimo"""
        return [prod for prod in self.produtos.values() if prod.abaixo_minimo()]
    
    def relatorio_minimo(self) -> None:
        """Exibe relatório de produtos abaixo do mínimo"""
        produtos_baixos = self.produtos_abaixo_minimo()
        
        if not produtos_baixos:
            print("\n✓ Todos os produtos estão acima do estoque mínimo!\n")
            return
        
        print("\n" + "="*80)
        print("PRODUTOS ABAIXO DO ESTOQUE MÍNIMO")
        print("="*80)
        
        for prod in produtos_baixos:
            print(f"ID: {prod.id_produto}")
            print(f"Nome: {prod.nome}")
            print(f"Quantidade atual: {prod.quantidade} | Mínimo: {prod.minimo}")
            print(f"Faltam: {prod.minimo - prod.quantidade} unidades")
            print("-"*80)
        
        print()
    
    def relatorio_valor_total(self) -> None:
        """Exibe o valor total do estoque"""
        valor_total = sum(prod.valor_total() for prod in self.produtos.values())
        quantidade_total = sum(prod.quantidade for prod in self.produtos.values())
        
        print("\n" + "="*50)
        print("RELATÓRIO DE VALOR DO ESTOQUE")
        print("="*50)
        print(f"Total de produtos: {len(self.produtos)}")
        print(f"Total de itens: {quantidade_total} unidades")
        print(f"Valor total: R${valor_total:.2f}")
        print("="*50 + "\n")
    
    def relatorio_por_categoria(self) -> None:
        """Exibe relatório agrupado por categoria"""
        categorias = {}
        
        for prod in self.produtos.values():
            if prod.categoria not in categorias:
                categorias[prod.categoria] = []
            categorias[prod.categoria].append(prod)
        
        if not categorias:
            print("\n✗ Nenhum produto cadastrado!\n")
            return
        
        print("\n" + "="*80)
        print("RELATÓRIO POR CATEGORIA")
        print("="*80)
        
        for categoria, produtos in sorted(categorias.items()):
            valor_categoria = sum(p.valor_total() for p in produtos)
            qtd_categoria = sum(p.quantidade for p in produtos)
            
            print(f"\n{categoria.upper()}")
            print(f"  Produtos: {len(produtos)} | Quantidade: {qtd_categoria} | Valor: R${valor_categoria:.2f}")
            
            for prod in produtos:
                print(f"    - {prod.nome:<30} Qtd: {prod.quantidade:<6} R${prod.valor_total():.2f}")
        
        print("\n" + "="*80 + "\n")


def menu_principal():
    """Menu principal do sistema"""
    estoque = Estoque()
    
    while True:
        print("\n" + "="*60)
        print("SISTEMA DE GESTÃO DE ESTOQUE".center(60))
        print("="*60)
        print("""
    1. Adicionar Produto
    2. Remover Produto
    3. Entrada de Estoque (Compra)
    4. Saída de Estoque (Venda)
    5. Listar Todos os Produtos
    6. Buscar Produto
    7. Produtos com Estoque Baixo
    8. Relatório de Valor Total
    9. Relatório por Categoria
    0. Sair
        """)
        print("="*60)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n--- ADICIONAR NOVO PRODUTO ---")
            id_prod = input("ID do Produto: ").strip()
            nome = input("Nome: ").strip()
            categoria = input("Categoria: ").strip()
            try:
                preco = float(input("Preço: R$"))
                quantidade = int(input("Quantidade: "))
                minimo = int(input("Estoque Mínimo: "))
                localizacao = input("Localização (opcional): ").strip()
                estoque.adicionar_produto(id_prod, nome, categoria, preco, 
                                        quantidade, minimo, localizacao)
            except ValueError:
                print("✗ Dados inválidos! Use números para preço e quantidade.")
        
        elif opcao == "2":
            print("\n--- REMOVER PRODUTO ---")
            id_prod = input("ID do Produto a remover: ").strip()
            estoque.remover_produto(id_prod)
        
        elif opcao == "3":
            print("\n--- ENTRADA DE ESTOQUE ---")
            id_prod = input("ID do Produto: ").strip()
            try:
                quantidade = int(input("Quantidade a adicionar: "))
                estoque.entrada_estoque(id_prod, quantidade)
            except ValueError:
                print("✗ Quantidade inválida!")
        
        elif opcao == "4":
            print("\n--- SAÍDA DE ESTOQUE ---")
            id_prod = input("ID do Produto: ").strip()
            try:
                quantidade = int(input("Quantidade a remover: "))
                estoque.saida_estoque(id_prod, quantidade)
            except ValueError:
                print("✗ Quantidade inválida!")
        
        elif opcao == "5":
            estoque.listar_produtos()
        
        elif opcao == "6":
            print("\n--- BUSCAR PRODUTO ---")
            id_prod = input("ID do Produto: ").strip()
            produto = estoque.buscar_produto(id_prod)
            if produto:
                print(f"\n{produto.nome} (ID: {produto.id_produto})")
                print(f"Categoria: {produto.categoria}")
                print(f"Preço: R${produto.preco:.2f}")
                print(f"Quantidade: {produto.quantidade} unidades")
                print(f"Estoque Mínimo: {produto.minimo} unidades")
                print(f"Localização: {produto.localizacao if produto.localizacao else 'Não especificada'}")
                print()
            else:
                print("✗ Produto não encontrado!")
        
        elif opcao == "7":
            estoque.relatorio_minimo()
        
        elif opcao == "8":
            estoque.relatorio_valor_total()
        
        elif opcao == "9":
            estoque.relatorio_por_categoria()
        
        elif opcao == "0":
            print("\nAté logo! Sistema encerrado.")
            break
        
        else:
            print("✗ Opção inválida!")


if __name__ == "__main__":
    menu_principal()
