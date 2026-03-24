# Frontend Web - Guia de Instalação Rápida

## 📋 O Que É?

Um **frontend web moderno e responsivo** para o Sistema de Gestão de Estoque. Interface visual completa com dashboard, gráficos e controles interativos.

## 🚀 Instalação em 3 Passos

### Passo 1: Descompactar Arquivo
Certifique-se de ter todos os arquivos no mesmo diretório.

### Passo 2: Instalar Dependências
Abra o terminal/CMD no diretório do projeto e execute:

```bash
pip install -r requirements.txt
```

### Passo 3: Iniciar o Servidor

**Windows:**
- Duplo clique em `iniciar_frontend.bat`

**macOS/Linux:**
```bash
python app.py
```

## 🌐 Acessar

Abra seu navegador em: **http://localhost:5000**

## 📁 Arquivos Novos/Modificados

### 🆕 Arquivos Criados

| Arquivo | Descrição |
|---------|-----------|
| `app.py` | API Flask (Backend do frontend) |
| `templates/index.html` | Interface HTML completa |
| `static/css/style.css` | Estilos e design responsivo |
| `static/js/app.js` | Lógica JavaScript interativa |
| `iniciar_frontend.bat` | Script para iniciar no Windows |
| `teste_frontend.py` | Script para testar o setup |

### 📝 Arquivos Modificados

| Arquivo | O Que Mudou |
|---------|-----------|
| `requirements.txt` | Adicionado Flask e Werkzeug |

## ✨ Funcionalidades do Frontend

- ✅ Dashboard com KPIs em tempo real
- ✅ Gráficos interativos (Pizza e Barras)
- ✅ Gerenciamento completo de produtos
- ✅ Busca e filtros rápidos
- ✅ Movimentação de estoque (entrada/saída)
- ✅ Relatórios por categoria e top produtos
- ✅ Alertas de estoque baixo
- ✅ Interface responsiva (desktop/tablet/mobile)
- ✅ Atualização automática de dados

## 🧪 Validar Instalação

Execute o script de teste:

```bash
python teste_frontend.py
```

Se tudo estiver OK, verá:
```
✓ TODOS OS TESTES PASSARAM COM SUCESSO!
```

## 🔧 Troubleshooting

### Erro: "Python não encontrado"
- Instale Python 3.6+ em https://www.python.org
- Adicione Python ao PATH

### Erro: "Módulo não encontrado"
```bash
pip install -r requirements.txt
```

### Erro: "Conexão recusada"
- O servidor pode não estar rodando
- Verifique se a janela do terminal/CMD está aberta
- Tente http://localhost:5000 novamente

### Porta 5000 em uso
Se a porta 5000 já está em uso:
1. Edite `app.py`
2. Procure por `app.run(...)`
3. Mude `port=5000` para `port=5001` (ou outra)
4. Reinicie a aplicação

## 📱 Como Usar

1. **Abra o Dashboard** - Veja seus dados em tempo real
2. **Adicione Produtos** - Clique em "+ Novo Produto"
3. **Gerencie Estoque** - Registre entradas e saídas
4. **Consulte Relatórios** - Analise seu estoque

## 🎯 Próximos Passos

1. Copie dados de exemplo (se aplicável):
   ```bash
   copy dados_estoque_exemplo.json dados_estoque.json
   ```

2. Inicie o servidor:
   - **Windows**: Duplo clique em `iniciar_frontend.bat`
   -**Outros**: `python app.py`

3. Abra em seu navegador: **http://localhost:5000**

## 📚 Documentação Completa

Veja `README_FRONTEND.md` para documentação detalhada.

## 💻 Requisitos

- **Python**: 3.6+
- **Navegador**: Chrome, Firefox, Safari ou Edge (moderno)
- **Espaço em Disco**: ~5 MB

## ⚡ Performance

- Atualização automática a cada 5 segundos
- Suporta até 1000+ produtos sem problemas
- Interface responsiva e rápida

## 🎓 Estrutura do Projeto

```
ESTOQUE TESTE/
├── app.py                    # API Flask
├── estoque.py               # Sistema de estoque (backend)
├── teste_frontend.py        # Script de teste
├── iniciar_frontend.bat     # Para iniciar no Windows
├── requirements.txt         # Dependências
├── dados_estoque.json       # Dados (criado automaticamente)
├── templates/
│   └── index.html          # Interface web
├── static/
│   ├── css/
│   │   └── style.css       # Estilos
│   └── js/
│       └── app.js          # JavaScript
└── README_FRONTEND.md      # Documentação completa
```

## 🆘 Precisa de Ajuda?

1. Verifique os logs no terminal
2. Execute `teste_frontend.py` para diagnosticar
3. Veja `README_FRONTEND.md` para FAQ

---

**Versão**: 1.0  
**Última atualização**: 2024  
**Status**: ✅ Pronto para usar
