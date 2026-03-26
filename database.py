import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Carregar variaveis de ambiente
load_dotenv()

# Configuracao do banco de dados
def get_database_url():
    """Obtem URL do banco com fallback para SQLite"""
    db_url = os.getenv('DATABASE_URL')
    
    if db_url and db_url.startswith('postgresql'):
        return db_url
    
    # Fallback para SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    return f'sqlite:///{os.path.join(basedir, "estoque.db")}'

DATABASE_URL = get_database_url()

# Instancia do SQLAlchemy
db = SQLAlchemy()

def create_app():
    """Factory function para criar a aplicacao Flask"""
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='/static')

    # Configuracoes
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave-secreta-desenvolvimento')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'check_same_thread': False} if 'sqlite' in DATABASE_URL else {}
    }

    # Inicializar banco de dados
    db.init_app(app)

    return app, db