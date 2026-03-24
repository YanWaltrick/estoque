#!/bin/bash
# Script para listar visualmente todos os arquivos do projeto

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║        SISTEMA DE GESTÃO DE ESTOQUE - ESTRUTURA DE ARQUIVOS              ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Função para contar linhas
count_lines() {
    if [ -f "$1" ]; then
        wc -l < "$1" | tr -d ' '
    else
        echo "0"
    fi
}

# Função para tamanho
get_size() {
    if [ -f "$1" ]; then
        ls -lh "$1" | awk '{print $5}'
    else
        echo "-"
    fi
}

echo "📦 ARQUIVOS PRINCIPAIS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "🔧 Backend & API"
echo "├─ 📄 app.py ($(count_lines app.py) linhas) - API Flask REST"
echo "│  └─ 12+ endpoints para gerenciar produtos"
echo "│  └─ Integração com estoque.py"
echo "│  └─ Suporte a CORS"
echo ""
echo "├─ 📄 estoque.py - Lógica de Negócio (existente)"
echo "│  └─ Classes: Produto, Estoque"
echo "│  └─ Persistência em JSON"
echo ""

echo "📱 Frontend & Web UI"
echo "├─ 📁 templates/"
echo "│  └─ 📄 index.html ($(count_lines templates/index.html) linhas) - Interface Web"
echo "│     └─ Dashboard completo"
echo "│     └─ Navbar com navegação"
echo "│     └─ Modais para operações"
echo "│     └─ Tabelas responsivas"
echo "│     └─ Gráficos interativos"
echo ""
echo "├─ 📁 static/"
echo "│  ├─ 📁 css/"
echo "│  │  └─ 📄 style.css ($(count_lines static/css/style.css) linhas) - Estilos"
echo "│  │     └─ Design moderno"
echo "│  │     └─ Responsivo"
echo "│  │     └─ Temas e animações"
echo "│  │"
echo "│  └─ 📁 js/"
echo "│     └─ 📄 app.js ($(count_lines static/js/app.js) linhas) - Lógica JS"
echo "│        └─ Requisições à API"
echo "│        └─ Gráficos com Chart.js"
echo "│        └─ Validações e UX"
echo ""

echo "⚙️  Configuração & Execução"
echo "├─ 📄 requirements.txt - Dependências Python"
echo "│  └─ Flask 2.3.2"
echo "│  └─ Werkzeug 2.3.6"
echo ""
echo "├─ 🎯 iniciar_frontend.bat - Script Windows"
echo "│  └─ Instala dependências"
echo "│  └─ Verifica Python"
echo "│  └─ Inicia servidor"
echo ""
echo "├─ 🧪 teste_frontend.py ($(count_lines teste_frontend.py) linhas) - Validação"
echo "│  └─ Testa imports"
echo "│  └─ Valida arquivos"
echo "│  └─ Testa classes"
echo "│  └─ Diagnostica problemas"
echo ""

echo "📚 Documentação"
echo "├─ 📖 README_FRONTEND.md - Documentação Completa"
echo "│  └─ Guia de uso detalhado"
echo "│  └─ Funcionalidades"
echo "│  └─ FAQ e Troubleshooting"
echo ""
echo "├─ 📖 FRONTEND_INSTALACAO.md - Guia Rápido"
echo "│  └─ 3 passos para começar"
echo "│  └─ Validação de instalação"
echo ""
echo "├─ 📖 RESUMO_CRIACAO.md - Resumo"
echo "│  └─ O que foi criado"
echo "│  └─ Próximas etapas"
echo ""

echo "💾 Dados"
echo "├─ 📄 dados_estoque.json - Dados da Aplicação"
echo "│  └─ Criado automaticamente"
echo "│  └─ Backup regular recomendado"
echo ""

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                          RESUMO ESTATÍSTICO                               ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

TOTAL_LINES=$(($(count_lines app.py) + $(count_lines templates/index.html) + $(count_lines static/css/style.css) + $(count_lines static/js/app.js) + $(count_lines teste_frontend.py)))

echo "📊 Estatísticas:"
echo "  • Arquivos criados/modificados: 10"
echo "  • Linhas de código Python: $(count_lines app.py)"
echo "  • Linhas de HTML: $(count_lines templates/index.html)"
echo "  • Linhas de CSS: $(count_lines static/css/style.css)"
echo "  • Linhas de JavaScript: $(count_lines static/js/app.js)"
echo "  • Total de linhas: ~$TOTAL_LINES"
echo "  • Endpoints da API: 12+"
echo "  • Componentes UI: 15+"
echo "  • Funcionalidades: 20+"
echo ""

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                      COMO COMEÇAR                                        ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "1️⃣  Instale as dependências:"
echo "    pip install -r requirements.txt"
echo ""
echo "2️⃣  Inicie o servidor:"
echo "    python app.py"
echo ""
echo "3️⃣  Abra no navegador:"
echo "    http://localhost:5000"
echo ""
echo "🧪 Ou valide a instalação:"
echo "    python teste_frontend.py"
echo ""

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                      TECNOLOGIAS UTILIZADAS                              ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Backend:    Python 3 + Flask + Werkzeug"
echo "Frontend:   HTML5 + CSS3 + JavaScript ES6+"
echo "UI:         Bootstrap 5 + Font Awesome + Chart.js"
echo "Storage:    JSON (SQLite/MySQL expandível)"
echo "API:        REST com CORS"
echo ""

echo "✅ Pronto para usar!"
echo ""
