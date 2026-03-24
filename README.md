# Sistema de Gestão de Estoque

Um sistema completo e profissional para gerenciar o estoque de sua empresa, desenvolvido em Python.

## 📋 Funcionalidades

✅ **Gerenciamento de Produtos**
- Adicionar novos produtos
- Remover produtos
- Buscar produtos por ID
- Listar todos os produtos

✅ **Controle de Estoque**
- Registrar entrada de produtos (compras)
- Registrar saída de produtos (vendas)
- Atualizar quantidades
- Definir estoque mínimo

✅ **Relatórios**
- Listar todos os produtos com detalhes
- Produtos com estoque baixo (alerta)
- Valor total do estoque
- Relatório agrupado por categoria

✅ **Persistência**
- Dados salvos automaticamente em JSON
- Recuperação de dados ao iniciar
- Backup automático dos dados

## 🚀 Como Usar

### 1. Executar o Sistema

```bash
python estoque.py
```

### 2. Menu Principal

O sistema oferece 10 opções:

| Opção | Função | Descrição |
|-------|--------|-----------|
| 1 | Adicionar Produto | Cadastra novo item no estoque |
| 2 | Remover Produto | Deleta um produto |
| 3 | Entrada de Estoque | Registra compra/recebimento |
| 4 | Saída de Estoque | Registra venda/saída |
| 5 | Listar Produtos | Mostra todos os itens |
| 6 | Buscar Produto | Procura por ID específico |
| 7 | Estoque Baixo | Alerta de reposição necessária |
| 8 | Valor Total | Mostra valor total do estoque |
| 9 | Por Categoria | Relatório organizado por tipo |
| 0 | Sair | Encerra o programa |

## 📝 Exemplo de Uso

### Adicionar um Produto
```
Opção: 1
ID do Produto: PROD001
Nome: Notebook Dell
Categoria: Informática
Preço: 3499.90
Quantidade: 5
Estoque Mínimo: 2
Localização: Prateleira A1
```

### Entrada de Estoque (Recebimento)
```
Opção: 3
ID do Produto: PROD001
Quantidade a adicionar: 10
```

### Saída de Estoque (Venda)
```
Opção: 4
ID do Produto: PROD001
Quantidade a remover: 3
```

## 💾 Dados

Os dados são armazenados automaticamente em `dados_estoque.json`:

```json
{
    "PROD001": {
        "id_produto": "PROD001",
        "nome": "Notebook Dell",
        "categoria": "Informática",
        "preco": 3499.90,
        "quantidade": 12,
        "minimo": 2,
        "localizacao": "Prateleira A1",
        "data_criacao": "20/03/2026 14:30:00"
    }
}
```

## 🔍 Informações de Cada Produto

- **ID**: Identificador único
- **Nome**: Nome do produto
- **Categoria**: Tipo de classificação
- **Preço**: Valor unitário
- **Quantidade**: Itens em estoque
- **Mínimo**: Limite para alerta
- **Localização**: Onde encontrar no estoque
- **Data**: Quando foi adicionado

## ⚙️ Requisitos

- Python 3.6+
- Nenhuma biblioteca externa necessária (usa bibliotecas padrão)

## 📊 Relatórios Disponíveis

### 1. Produtos com Estoque Baixo
Mostra todos os produtos com quantidade abaixo do mínimo especificado.

### 2. Valor Total do Estoque
Calcula o valor total investido em produtos.

### 3. Relatório por Categoria
Agrupa produtos por categoria com totalizações.

## 🎯 Dicas de Uso

1. **Sempre defina um ID único** para cada produto
2. **Use categorias consistentes** para melhor organização
3. **Defina estoque mínimo** para receber alertas automaticamente
4. **Revise relatórios regularmente** para decisões de reposição
5. **Adicione localização** para facilitar localização física

## 🔧 Estrutura do Código

### Classe `Produto`
Representa um item individual no estoque com seus atributos e métodos.

### Classe `Estoque`
Gerencia a coleção de produtos e operações do sistema.

### Função `menu_principal()`
Interface interativa com o usuário.

## 📱 Próximas Melhorias (Sugestões)

- [ ] Interface gráfica (tkinter ou web)
- [ ] Banco de dados relacional (SQLite/MySQL)
- [ ] Histórico de movimentações
- [ ] Gráficos e análises
- [ ] Sistema de múltiplos usuários
- [ ] Backup automático na nuvem
- [ ] Integração com fornecedores
- [ ] Código de barras/QR Code

---

**Desenvolvido para gestão eficiente de estoque!** 📦✨
