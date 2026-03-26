from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text
from database import create_app, db, DATABASE_URL
from estoque_db import EstoqueDB
from models import Produto, Movimentacao, User
import os

# Criar aplicacao Flask
app, db = create_app()

# Exibir informacoes de configuracao
print("\n" + "="*60)
print("Sistema de Estoque - Inicializando...")
print("="*60)
db_type = "PostgreSQL" if "postgresql" in DATABASE_URL else "SQLite"
print(f"Banco de dados: {db_type}")
if db_type == "SQLite":
    print("Info: PostgreSQL nao encontrado. Usando SQLite local.")
    print("      Para usar PostgreSQL, instale e configure em .env")
print("="*60 + "\n")

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faca login para acessar esta pagina.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Instância global do estoque (será inicializada depois)
estoque = None
# ============================================================================
# ROTAS - AUTENTICAÇÃO
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin():
    """Página de administração de usuários (apenas para admins)"""
    if not current_user.is_admin:
        flash('Acesso negado. Apenas administradores podem acessar esta página.', 'error')
        return redirect(url_for('index'))
    return render_template('admin.html')

# ============================================================================
# ROTAS - API DE USUÁRIOS
# ============================================================================

@app.route('/api/users', methods=['GET'])
@login_required
def get_users():
    """Retorna lista de usuários (apenas para admins)"""
    if not current_user.is_admin:
        return jsonify({'erro': 'Acesso negado'}), 403
    
    users = User.query.all()
    resultado = []
    for user in users:
        resultado.append({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'data_criacao': user.data_criacao.strftime("%d/%m/%Y %H:%M:%S") if user.data_criacao else None
        })
    return jsonify(resultado)

@app.route('/api/users', methods=['POST'])
@login_required
def criar_user():
    """Cria um novo usuário (apenas para admins)"""
    if not current_user.is_admin:
        return jsonify({'erro': 'Acesso negado'}), 403
    
    dados = request.get_json()
    username = dados.get('username')
    password = dados.get('password')
    role = dados.get('role', 'user')
    
    if not username or not password:
        return jsonify({'erro': 'Username e password são obrigatórios'}), 400
    
    if role not in ['user', 'admin']:
        return jsonify({'erro': 'Role deve ser "user" ou "admin"'}), 400
    
    # Verificar se username já existe
    if User.query.filter_by(username=username).first():
        return jsonify({'erro': 'Username já existe'}), 400
    
    novo_user = User(username=username, password=generate_password_hash(password), role=role)
    db.session.add(novo_user)
    db.session.commit()
    
    return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@login_required
def deletar_user(user_id):
    """Remove um usuário (apenas para admins)"""
    if not current_user.is_admin:
        return jsonify({'erro': 'Acesso negado'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    # Não permitir deletar o próprio usuário
    if user.id == current_user.id:
        return jsonify({'erro': 'Não é possível deletar o próprio usuário'}), 400
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'mensagem': 'Usuário removido com sucesso'})

# ============================================================================
# ROTAS - PÁGINA PRINCIPAL
# ============================================================================

@app.route('/')
@login_required
def index():
    """Página principal do dashboard"""
    return render_template('index.html')


# ============================================================================
# ROTAS - API DE PRODUTOS
# ============================================================================

@app.route('/api/produtos', methods=['GET'])
@login_required
def get_produtos():
    """Retorna lista de todos os produtos"""
    try:
        produtos = estoque.listar_produtos()
        return jsonify([prod.to_dict() for prod in produtos])
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


def validar_dados_produto(dados, atualizar=False):
    erros = []

    if not dados:
        erros.append('JSON inválido ou vazio')
        return erros

    id_produto = dados.get('id') if not atualizar else None
    nome = dados.get('nome')
    categoria = dados.get('categoria')
    preco = dados.get('preco')
    quantidade = dados.get('quantidade')
    minimo = dados.get('minimo')

    if not atualizar:
        if not id_produto or not str(id_produto).strip():
            erros.append('ID do produto é obrigatório')

    if not nome or not str(nome).strip():
        erros.append('Nome é obrigatório')

    if not categoria or not str(categoria).strip():
        erros.append('Categoria é obrigatória')

    try:
        preco = float(preco)
        if preco < 0:
            erros.append('Preço não pode ser negativo')
    except Exception:
        erros.append('Preço inválido')

    try:
        quantidade = int(quantidade)
        if quantidade < 0:
            erros.append('Quantidade não pode ser negativa')
    except Exception:
        erros.append('Quantidade inválida')

    try:
        minimo = int(minimo)
        if minimo < 0:
            erros.append('Mínimo não pode ser negativo')
    except Exception:
        erros.append('Mínimo inválido')

    return erros


@app.route('/api/produtos/<id_produto>', methods=['GET'])
@login_required
def get_produto(id_produto):
    """Retorna um produto específico"""
    try:
        produto = estoque.buscar_produto(id_produto)
        if not produto:
            return jsonify({'erro': 'Produto não encontrado'}), 404

        return jsonify(produto.to_dict())
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/produtos', methods=['POST'])
@login_required
def criar_produto():
    """Cria um novo produto"""
    try:
        dados = request.get_json()
        erros = validar_dados_produto(dados, atualizar=False)
        if erros:
            return jsonify({'erro': ' | '.join(erros)}), 400

        sucesso = estoque.adicionar_produto(
            id_produto=str(dados['id']).strip(),
            nome=str(dados['nome']).strip(),
            categoria=str(dados['categoria']).strip(),
            preco=float(dados['preco']),
            quantidade=int(dados['quantidade']),
            minimo=int(dados['minimo']),
            localizacao=str(dados.get('localizacao', '')).strip()
        )

        if sucesso:
            return jsonify({'mensagem': 'Produto criado com sucesso'}), 201
        else:
            return jsonify({'erro': 'Falha ao criar produto'}), 400

    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/produtos/<id_produto>', methods=['PUT'])
@login_required
def atualizar_produto(id_produto):
    """Atualiza um produto"""
    dados = request.get_json()
    produto = estoque.buscar_produto(id_produto)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404

    erros = validar_dados_produto(dados, atualizar=True)
    if erros:
        return jsonify({'erro': ' | '.join(erros)}), 400

    try:
        dados_update = {
            'nome': str(dados['nome']).strip(),
            'categoria': str(dados['categoria']).strip(),
            'preco': float(dados['preco']),
            'quantidade': int(dados['quantidade']),
            'minimo': int(dados['minimo']),
            'localizacao': str(dados.get('localizacao', '')).strip()
        }

        sucesso = estoque.atualizar_produto(id_produto, **dados_update)
        if not sucesso:
            return jsonify({'erro': 'Falha ao atualizar produto'}), 400

        produto_atualizado = estoque.buscar_produto(id_produto)
        return jsonify({
            'mensagem': 'Produto atualizado com sucesso',
            'produto': produto_atualizado.to_dict()
        })

    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/produtos/<id_produto>', methods=['DELETE'])
@login_required
def deletar_produto(id_produto):
    """Delete um produto"""
    try:
        sucesso = estoque.remover_produto(id_produto)

        if sucesso:
            return jsonify({'mensagem': 'Produto removido com sucesso'})
        else:
            return jsonify({'erro': 'Produto não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ============================================================================
# ROTAS - MOVIMENTAÇÕES DE ESTOQUE
# ============================================================================

@app.route('/api/entrada', methods=['POST'])
@login_required
def entrada_estoque():
    """Registra entrada de produtos"""
    try:
        dados = request.get_json()

        sucesso = estoque.entrada_estoque(
            id_produto=dados['id'],
            quantidade=int(dados['quantidade']),
            motivo=dados.get('motivo', ''),
            usuario=dados.get('usuario', '')
        )

        if sucesso:
            return jsonify({'mensagem': 'Entrada registrada com sucesso'})
        else:
            return jsonify({'erro': 'Falha ao registrar entrada'}), 400

    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/saida', methods=['POST'])
@login_required
def saida_estoque():
    """Registra saída de produtos"""
    try:
        dados = request.get_json()

        sucesso = estoque.saida_estoque(
            id_produto=dados['id'],
            quantidade=int(dados['quantidade']),
            motivo=dados.get('motivo', ''),
            usuario=dados.get('usuario', '')
        )

        if sucesso:
            return jsonify({'mensagem': 'Saída registrada com sucesso'})
        else:
            return jsonify({'erro': 'Falha ao registrar saída'}), 400

    except Exception as e:
        return jsonify({'erro': str(e)}), 400


# ============================================================================
# ROTAS - RELATÓRIOS
# ============================================================================

@app.route('/api/relatorios/resumo', methods=['GET'])
@login_required
def relatorio_resumo():
    """Retorna resumo do estoque"""
    try:
        estatisticas = estoque.relatorio_valor_total()
        produtos_baixo = len(estoque.relatorio_estoque_baixo())

        # Contar categorias únicas
        produtos = estoque.listar_produtos()
        total_categorias = len(set(p.categoria for p in produtos))

        return jsonify({
            'total_produtos': estatisticas['total_produtos'],
            'total_quantidades': estatisticas['total_unidades'],
            'valor_total': estatisticas['valor_total'],
            'produtos_estoque_baixo': produtos_baixo,
            'total_categorias': total_categorias
        })
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/relatorios/estoque-baixo', methods=['GET'])
@login_required
def relatorio_estoque_baixo():
    """Retorna produtos com estoque baixo"""
    try:
        produtos_baixos = estoque.relatorio_estoque_baixo()

        resultado = []
        for prod in produtos_baixos:
            resultado.append({
                'id': prod.id_produto,
                'nome': prod.nome,
                'quantidade': prod.quantidade,
                'minimo': prod.minimo,
                'faltam': prod.minimo - prod.quantidade,
                'categoria': prod.categoria
            })

        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/relatorios/por-categoria', methods=['GET'])
@login_required
def relatorio_por_categoria():
    """Retorna relatório agrupado por categoria"""
    try:
        categorias = estoque.relatorio_por_categoria()

        resultado = []
        for categoria, dados in sorted(categorias.items()):
            resultado.append({
                'categoria': categoria,
                'quantidade': dados['total_unidades'],
                'valor_total': dados['valor_total'],
                'produtos': dados['total_produtos']
            })

        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@app.route('/api/relatorios/top-produtos', methods=['GET'])
@login_required
def relatorio_top_produtos():
    """Retorna top 10 produtos por valor"""
    try:
        produtos = estoque.listar_produtos()
        produtos_sorted = sorted(produtos, key=lambda p: p.valor_total(), reverse=True)[:10]

        resultado = []
        for prod in produtos_sorted:
            resultado.append({
                'id': prod.id_produto,
                'nome': prod.nome,
                'valor_total': prod.valor_total(),
                'quantidade': prod.quantidade,
                'preco': prod.preco
            })

        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


# ============================================================================
# TRATAMENTO DE ERROS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Erro 404"""
    return jsonify({'erro': 'Endpoint não encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Erro 500"""
    return jsonify({'erro': 'Erro interno do servidor'}), 500


# ============================================================================
# INICIALIZAÇÃO DO BANCO DE DADOS
# ============================================================================

def init_db():
    """Inicializa o banco de dados e cria as tabelas"""
    global estoque
    with app.app_context():
        try:
            db.create_all()
            print("Tabelas do banco criadas/verificadas")

            # Verificar coluna role apenas para SQLite
            if db.engine.dialect.name == 'sqlite':
                try:
                    with db.engine.connect() as conn:
                        coluna_role = conn.execute(text("PRAGMA table_info(users)"))
                        coluna_role = coluna_role.fetchall()
                        if coluna_role and 'role' not in [c[1] for c in coluna_role]:
                            conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'user'"))
                            conn.commit()
                except:
                    pass

            # Criar usuario admin se nao existir
            admin_user = User.query.filter_by(username='admin').first()
            if not admin_user:
                admin_user = User(username='admin', password=generate_password_hash('admin'), role='admin')
                db.session.add(admin_user)
                db.session.commit()
                print("Usuario admin criado (login: admin / senha: admin)")
            else:
                # Se existir mas nao tiver role, atualiza
                if not admin_user.role or admin_user.role not in ['user', 'admin']:
                    admin_user.role = 'admin'
                    db.session.commit()

            # Inicializar o estoque
            estoque = EstoqueDB()
            print("Banco de dados inicializado com sucesso\n")
            
        except Exception as erro:
            print(f"ERRO ao inicializar banco: {erro}")
            print("Verificar: PostgreSQL rodando? Credenciais corretas? Banco criado?")
            raise

# Inicializar banco de dados na primeira execução
init_db()

# ============================================================================
# EXECUTAR APLICAÇÃO
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
