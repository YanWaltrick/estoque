# Sistema de Gestão de Estoque - Frontend Web

## 📱 Visão Geral

O **Frontend Web** é uma interface moderna e intuitiva para gerenciar seu estoque. Ele oferece um dashboard completo com gráficos, relatórios e controles para todas as operações de estoque.

## ✨ Funcionalidades

### Dashboard
- **KPIs em Tempo Real**: Total de produtos, quantidade total, valor total, produtos com estoque baixo
- **Gráficos Interativos**: 
  - Distribuição por categoria (Pizza)
  - Top 10 produtos por valor (Barras)
- **Alertas de Estoque**: Visualização imediata de produtos com estoque baixo
- **Atualização Automática**: Dados atualizados a cada 5 segundos

### Gerenciamento de Produtos
- **Adicionar Produtos**: Formulário intuitivo para cadastrar novos itens
- **Editar Produtos**: Modificar informações de produtos existentes
- **Deletar Produtos**: Remover produtos do estoque
- **Busca Rápida**: Filtrar produtos por ID, nome ou categoria
- **Movimentações**: Registrar entrada e saída de estoque

### Relatórios
- **Por Categoria**: Agrupamento de produtos, quantidades e valores
- **Top Produtos**: Os 10 produtos com maior valor total em estoque

## 🚀 Como Iniciar

### Opção 1: Iniciar via Arquivo .BAT (Windows)

1. Abra o arquivo **iniciar_frontend.bat** com duplo clique
2. O script irá:
   - Verificar se Python está instalado
   - Instalar as dependências necessárias
   - Copiar dados de exemplo (se necessário)
   - Iniciar o servidor web

3. Abra seu navegador em: **http://localhost:5000**

### Opção 2: Iniciar via Terminal

```bash
# 1. Instalar dependências (primeira vez)
pip install -r requirements.txt

# 2. Executar o servidor
python app.py
```

3. O servidor irá iniciar em **http://localhost:5000**

## 📊 Usando o Dashboard

### Dashboard (Home)
- Visualize os KPIs principais
- Veja os gráficos de distribuição
- Receba alertas de estoque baixo
- Clique nos produtos com estoque baixo para registrar entrada

### Gerenciar Produtos
1. Clique em **"Produtos"** na barra de navegação
2. Use o campo de busca para encontrar produtos
3. Clique nos botões de ação:
   - ✏️ **Editar**: Modificar dados do produto
   - 🔄 **Movimentar**: Registrar entrada ou saída
   - 🗑️ **Deletar**: Remover produto

### Novo Produto
1. Clique no botão **"+ Novo Produto"**
2. Preencha os campos obrigatórios (*)
3. Clique em **"Salvar"**

**Campos do Produto:**
- **ID**: Identificador único (ex: PROD001)
- **Nome**: Nome do produto
- **Categoria**: Tipo/categoria do produto
- **Preço**: Valor unitário (R$)
- **Quantidade**: Quantidade em estoque
- **Estoque Mínimo**: Quantidade mínima recomendada
- **Localização**: Localização no armazém (opcional)

### Movimentações
1. Clique no botão 🔄 ao lado do produto
2. Escolha o tipo:
   - **Entrada**: Registrar compra/recebimento
   - **Saída**: Registrar venda/saída
3. Insira a quantidade
4. Clique em **"Confirmar"**

### Relatórios
1. Clique em **"Relatórios"** na barra de navegação
2. Escolha entre:
   - **Por Categoria**: Resumo agrupado por categoria
   - **Top Produtos**: Os 10 produtos mais valiosos

## 🔒 Dados e Persistência

- Os dados são armazenados em **dados_estoque.json**
- A aplicação carrega os dados automaticamente ao iniciar
- As alterações são salvas instantaneamente no arquivo
- Faça backup regularmente do arquivo **dados_estoque.json**

## ⚙️ Requisitos

- **Python**: 3.6 ou superior
- **Dependências**:
  - Flask 2.3.2
  - Werkzeug 2.3.6

## 🐛 Troubleshooting

### Erro: "Python não está instalado"
- Instale Python 3.6+ em https://www.python.org
- Marque "Add Python to PATH" durante a instalação
- Reinicie seu computador

### Erro: "Conexão recusada" ao abrir http://localhost:5000
- Verifique se o servidor está rodando (janela do terminal)
- Tente reabrir em alguns segundos
- Verifique se a porta 5000 não está em uso

### Erro: "Módulo não encontrado"
- Instale as dependências:
```bash
pip install -r requirements.txt
```

### Dados não aparecem
- Verifique se o arquivo **dados_estoque.json** existe
- Se não existir, copie **dados_estoque_exemplo.json**:
```bash
copy dados_estoque_exemplo.json dados_estoque.json
```

## 📱 Navegação no Mobile

O frontend é responsivo e funciona em:
- Desktop (Chrome, Firefox, Safari, Edge)
- Tablets
- Smartphones (recomendado em modo paisagem para melhor visualização)

## 🎨 Interface

### Cores e Temas
- **Azul**: Ações primárias e informações
- **Verde**: Sucesso e alertas positivos
- **Vermelho**: Perigo e alertas críticos
- **Amarelo**: Avisos e atenção

### Status de Produtos
- 🟢 **OK**: Quantidade dentro do esperado
- 🔴 **BAIXO**: Quantidade abaixo do mínimo (alerta para reposição)

## 📞 API REST

O frontend utiliza uma API REST interna. Os endpoints disponíveis são:

### Produtos
- `GET /api/produtos` - Listar todos
- `POST /api/produtos` - Criar novo
- `PUT /api/produtos/{id}` - Atualizar
- `DELETE /api/produtos/{id}` - Deletar

### Movimentações
- `POST /api/entrada` - Registrar entrada
- `POST /api/saida` - Registrar saída

### Relatórios
- `GET /api/relatorios/resumo` - KPIs
- `GET /api/relatorios/estoque-baixo` - Produtos low stock
- `GET /api/relatorios/por-categoria` - Agrupado por categoria
- `GET /api/relatorios/top-produtos` - Top 10

## 💡 Dicas

1. **Atualizações Automáticas**: O dashboard atualiza automaticamente a cada 5 segundos
2. **Busca em Tempo Real**: A busca filtra conforme você digita
3. **Atalhos**: Use Tab para navegar entre campos
4. **Backup**: Faça backup regular do arquivo dados_estoque.json
5. **Performance**: Para mais de 1000 produtos, considere usar um banco de dados

## 📝 Guia Rápido

| Ação | Como Fazer |
|------|-----------|
| Ver Dashboard | Clique em "Dashboard" na navbar |
| Adicionar Produto | Clique em "+ Novo Produto" |
| Buscar Produto | Use o campo "Buscar produto..." |
| Movimento Estoque | Clique no ícone 🔄 do produto |
| Ver Relatórios | Clique em "Relatórios" na navbar |
| Editar Produto | Clique no ícone ✏️ do produto |
| Deletar Produto | Clique no ícone 🗑️ e confirme |

## 🔄 Fluxo de Trabalho Típico

1. **Abra o Dashboard**: Veja o resumo do estoque
2. **Identifique Produtos com Estoque Baixo**: Veja na seção de alertas
3. **Registre Entradas**: Para produtos que chegaram de fornecedores
4. **Registre Saídas**: Para produtos vendidos
5. **Consulte Relatórios**: Analise a saúde do estoque
6. **Faça Backup dos Dados**: Regularmente

## 📜 Licença

Este projeto é parte do Sistema de Gestão de Estoque.

---

**Versão**: 1.0  
**Última atualização**: 2024  
**Desenvolvido em**: Python + Flask + Bootstrap
