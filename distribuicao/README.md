# Sistema de Estoque - Executável Windows

## 📦 Sobre o Executável

Este executável contém todo o sistema de gestão de estoque em um único arquivo `.exe` que pode ser executado em qualquer computador Windows sem necessidade de instalar Python ou outras dependências.

## 🚀 Como Usar

### Instalação:
1. Copie o arquivo `SistemaEstoque.exe` para o local desejado no seu computador
2. Execute o arquivo duplo-clicando nele

### Primeiro Uso:
- O sistema será iniciado automaticamente
- Um navegador web será aberto em `http://localhost:5000`
- O banco de dados SQLite será criado automaticamente na primeira execução

## ✨ Funcionalidades Incluídas

- ✅ Interface web completa
- ✅ Banco de dados SQLite integrado
- ✅ Gestão completa de produtos
- ✅ Relatórios de estoque
- ✅ Movimentações de entrada/saída
- ✅ Histórico de operações

## 📊 Dados Incluídos

O executável inclui:
- Todos os templates HTML
- Arquivos CSS e JavaScript
- Banco de dados SQLite com estrutura completa
- Todas as dependências Python necessárias

## 🔧 Requisitos do Sistema

- Windows 7 ou superior
- Não requer instalação de Python
- Não requer instalação de banco de dados
- Funciona offline

## 📁 Estrutura de Arquivos

Quando executado, o sistema cria:
- `estoque.db` - Banco de dados SQLite (se não existir)
- Servidor web local na porta 5000

## 🛠 Suporte

Se encontrar problemas:
1. Certifique-se de que a porta 5000 não está sendo usada por outro programa
2. Execute como administrador se houver problemas de permissão
3. Verifique se há antivírus bloqueando a execução

## 📝 Desenvolvimento

Para modificar o código fonte, use os arquivos originais:
- `app.py` - Aplicação principal
- `models.py` - Modelos do banco de dados
- `estoque_db.py` - Lógica de negócio
- `launcher.py` - Script de inicialização

Para gerar um novo executável, execute: `build_exe.bat`

---

**Criado com PyInstaller - Sistema de Estoque v1.0**