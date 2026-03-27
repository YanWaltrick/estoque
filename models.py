from datetime import datetime
from database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """Modelo para usuários do sistema"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # 'user' ou 'admin'
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, role='user'):
        self.username = username
        self.password = password
        self.role = role

    @property
    def is_admin(self):
        return self.role == 'admin'


class Produto(db.Model):
    """Modelo para produtos do estoque"""
    __tablename__ = 'produtos'

    id_produto = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    minimo = db.Column(db.Integer, nullable=False, default=0)
    localizacao = db.Column(db.String(255))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com movimentações
    movimentacoes = db.relationship('Movimentacao', backref='produto', lazy=True, cascade='all, delete-orphan')

    def __init__(self, id_produto, nome, categoria, preco, quantidade, minimo, localizacao=""):
        self.id_produto = id_produto
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.quantidade = quantidade
        self.minimo = minimo
        self.localizacao = localizacao

    def to_dict(self):
        """Converte o produto para dicionário"""
        return {
            'id': self.id_produto,
            'nome': self.nome,
            'categoria': self.categoria,
            'preco': self.preco,
            'quantidade': self.quantidade,
            'minimo': self.minimo,
            'localizacao': self.localizacao,
            'valor_total': self.valor_total(),
            'abaixo_minimo': self.abaixo_minimo(),
            'data_criacao': self.data_criacao.strftime("%d/%m/%Y %H:%M:%S") if self.data_criacao else None,
            'data_atualizacao': self.data_atualizacao.strftime("%d/%m/%Y %H:%M:%S") if self.data_atualizacao else None
        }

    def valor_total(self):
        """Calcula o valor total do produto em estoque"""
        return self.quantidade * self.preco

    def abaixo_minimo(self):
        """Verifica se o produto está abaixo do estoque mínimo"""
        return self.quantidade < self.minimo


class Movimentacao(db.Model):
    """Modelo para histórico de movimentações"""
    __tablename__ = 'movimentacoes'

    id_movimentacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_produto = db.Column(db.String(50), db.ForeignKey('produtos.id_produto'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'ENTRADA' ou 'SAIDA'
    quantidade = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(255))
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.Column(db.String(100))

    def __init__(self, id_produto, tipo, quantidade, motivo="", usuario=""):
        self.id_produto = id_produto
        self.tipo = tipo
        self.quantidade = quantidade
        self.motivo = motivo
        self.usuario = usuario


class Categoria(db.Model):
    """Modelo para categorias de produtos"""
    __tablename__ = 'categorias'

    id_categoria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    descricao = db.Column(db.String(255))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nome, descricao=""):
        self.nome = nome
        self.descricao = descricao


class Chamada(db.Model):
    """Modelo para chamadas/notificações de usuários para admins"""
    __tablename__ = 'chamadas'

    id_chamada = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)

    # Relacionamento com usuário
    usuario = db.relationship('User', backref='chamadas')

    def __init__(self, id_usuario, mensagem):
        self.id_usuario = id_usuario
        self.mensagem = mensagem

    def to_dict(self):
        return {
            'id': self.id_chamada,
            'id_usuario': self.id_usuario,
            'usuario': self.usuario.username if self.usuario else 'Desconhecido',
            'mensagem': self.mensagem,
            'data_criacao': self.data_criacao.strftime("%d/%m/%Y %H:%M:%S") if self.data_criacao else None,
            'lida': self.lida
        }