from database import create_app, db
from models import User
from werkzeug.security import generate_password_hash

app, _ = create_app()
with app.app_context():
    # Deleta o admin antigo se ele existir para não dar erro
    User.query.filter_by(username='admin2').delete()

    # Cria o novo admin com um método de hash compatível
    novo_admin = User(
        username='admin2',
        password=generate_password_hash('admin2', method='pbkdf2:sha256'),
        role='admin'
    )
    db.session.add(novo_admin)
    db.session.commit()
    print("Sucesso! Usuário 'admin2' com senha 'admin2' foi criado.")