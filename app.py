from flask import Flask, render_template, request, jsonify
from estoque import Estoque, Produto
import os

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

# Instância global do estoque
estoque = Estoque()

# ============================================================================
# ROTAS - PÁGINA PRINCIPAL
# ============================================================================

@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('index.html')


# ============================================================================
# ROTAS - API DE PRODUTOS
# ============================================================================

@app.route('/api/produtos', methods=['GET'])
def get_produtos():
    """Retorna lista de todos os produtos"""
    produtos = []
    for prod in estoque.produtos.values():
        produtos.append({
            'id': prod.id_produto,
            'nome': prod.nome,
            'categoria': prod.categoria,
            'preco': prod.preco,
            'quantidade': prod.quantidade,
            'minimo': prod.minimo,
            'localizacao': prod.localizacao,
            'valor_total': prod.valor_total(),
            'abaixo_minimo': prod.abaixo_minimo(),
            'data_criacao': prod.data_criacao
        })
    return jsonify(produtos)


@app.route('/api/produtos/<id_produto>', methods=['GET'])
def get_produto(id_produto):
    """Retorna um produto específico"""
    produto = estoque.buscar_produto(id_produto)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    return jsonify({
        'id': produto.id_produto,
        'nome': produto.nome,
        'categoria': produto.categoria,
        'preco': produto.preco,
        'quantidade': produto.quantidade,
        'minimo': produto.minimo,
        'localizacao': produto.localizacao,
        'valor_total': produto.valor_total(),
        'abaixo_minimo': produto.abaixo_minimo(),
        'data_criacao': produto.data_criacao
    })


@app.route('/api/produtos', methods=['POST'])
def criar_produto():
    """Cria um novo produto"""
    dados = request.get_json()
    
    try:
        sucesso = estoque.adicionar_produto(
            id_produto=dados['id'],
            nome=dados['nome'],
            categoria=dados['categoria'],
            preco=float(dados['preco']),
            quantidade=int(dados['quantidade']),
            minimo=int(dados['minimo']),
            localizacao=dados.get('localizacao', '')
        )
        
        if sucesso:
            return jsonify({'mensagem': 'Produto criado com sucesso'}), 201
        else:
            return jsonify({'erro': 'Falha ao criar produto'}), 400
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/produtos/<id_produto>', methods=['PUT'])
def atualizar_produto(id_produto):
    """Atualiza um produto"""
    dados = request.get_json()
    produto = estoque.buscar_produto(id_produto)
    
    if not produto:
        return jsonify({'erro': 'Produto não encontrado'}), 404
    
    try:
        # Atualiza campos se fornecidos
        if 'nome' in dados:
            produto.nome = dados['nome']
        if 'categoria' in dados:
            produto.categoria = dados['categoria']
        if 'preco' in dados:
            produto.preco = float(dados['preco'])
        if 'minimo' in dados:
            produto.minimo = int(dados['minimo'])
        if 'localizacao' in dados:
            produto.localizacao = dados['localizacao']
        
        estoque.salvar_dados()
        return jsonify({'mensagem': 'Produto atualizado com sucesso'})
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/produtos/<id_produto>', methods=['DELETE'])
def deletar_produto(id_produto):
    """Delete um produto"""
    sucesso = estoque.remover_produto(id_produto)
    
    if sucesso:
        return jsonify({'mensagem': 'Produto removido com sucesso'})
    else:
        return jsonify({'erro': 'Produto não encontrado'}), 404


# ============================================================================
# ROTAS - MOVIMENTAÇÕES DE ESTOQUE
# ============================================================================

@app.route('/api/entrada', methods=['POST'])
def entrada_estoque():
    """Registra entrada de produtos"""
    dados = request.get_json()
    
    try:
        sucesso = estoque.entrada_estoque(
            id_produto=dados['id'],
            quantidade=int(dados['quantidade'])
        )
        
        if sucesso:
            return jsonify({'mensagem': 'Entrada registrada com sucesso'})
        else:
            return jsonify({'erro': 'Falha ao registrar entrada'}), 400
            
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/saida', methods=['POST'])
def saida_estoque():
    """Registra saída de produtos"""
    dados = request.get_json()
    
    try:
        sucesso = estoque.saida_estoque(
            id_produto=dados['id'],
            quantidade=int(dados['quantidade'])
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
def relatorio_resumo():
    """Retorna resumo do estoque"""
    produtos = list(estoque.produtos.values())
    
    valor_total = sum(p.valor_total() for p in produtos)
    quantidade_total = sum(p.quantidade for p in produtos)
    produtos_baixo = len(estoque.produtos_abaixo_minimo())
    total_categorias = len(set(p.categoria for p in produtos))
    
    return jsonify({
        'total_produtos': len(produtos),
        'total_quantidades': quantidade_total,
        'valor_total': valor_total,
        'produtos_estoque_baixo': produtos_baixo,
        'total_categorias': total_categorias
    })


@app.route('/api/relatorios/estoque-baixo', methods=['GET'])
def relatorio_estoque_baixo():
    """Retorna produtos com estoque baixo"""
    produtos_baixos = estoque.produtos_abaixo_minimo()
    
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


@app.route('/api/relatorios/por-categoria', methods=['GET'])
def relatorio_por_categoria():
    """Retorna relatório agrupado por categoria"""
    categorias = {}
    
    for prod in estoque.produtos.values():
        if prod.categoria not in categorias:
            categorias[prod.categoria] = {
                'quantidade': 0,
                'valor_total': 0,
                'produtos': 0
            }
        
        categorias[prod.categoria]['quantidade'] += prod.quantidade
        categorias[prod.categoria]['valor_total'] += prod.valor_total()
        categorias[prod.categoria]['produtos'] += 1
    
    resultado = []
    for categoria, dados in sorted(categorias.items()):
        resultado.append({
            'categoria': categoria,
            'quantidade': dados['quantidade'],
            'valor_total': dados['valor_total'],
            'produtos': dados['produtos']
        })
    
    return jsonify(resultado)


@app.route('/api/relatorios/top-produtos', methods=['GET'])
def relatorio_top_produtos():
    """Retorna top 10 produtos por valor"""
    produtos = list(estoque.produtos.values())
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
# EXECUTAR APLICAÇÃO
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
