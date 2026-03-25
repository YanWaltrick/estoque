import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = f'sqlite:///{os.path.join(basedir, "estoque.db")}'

# Instância do SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='/static')

    # Configurações
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar banco de dados
    db.init_app(app)

    return app, db