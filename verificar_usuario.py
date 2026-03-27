from database import create_app, db
from models import User
from werkzeug.security import check_password_hash

app, _ = create_app()
with app.app_context():
    users = User.query.all()
    print("Usuários no banco:")
    for u in users:
        print(f"- {u.username}, role={u.role}, password_hash={u.password}")

    username = 'admin2'
    senha = 'admin2'
    user = User.query.filter_by(username=username).first()
    if user:
        ok = check_password_hash(user.password, senha)
        print(f"Verificação para {username}: {ok}")
    else:
        print(f"Usuário {username} não encontrado")
