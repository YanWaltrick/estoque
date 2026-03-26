# Guia Rápido - Sistema de Estoque com PostgreSQL

## ✓ Código Already Updated!

O código foi atualizado para usar PostgreSQL centralizado. Todos os arquivos já estão configurados.

---

## 📋 Passo 1: Instalar PostgreSQL

Execute o script de instalação automático:

```bash
instalar_postgresql.bat
```

**Ou siga manualmente:**
1. Baixe de: https://www.postgresql.org/download/windows/
2. Instale normalmente (senha: `12345` para o usuário `postgres`)
3. Abra PowerShell como Admin e execute:

```bash
psql -U postgres
CREATE USER estoque_user WITH PASSWORD '12345';
CREATE DATABASE estoque_db OWNER estoque_user;
GRANT ALL PRIVILEGES ON DATABASE estoque_db TO estoque_user;
\q
```

---

## 🔧 Passo 2: Configurar .env (Já Criado!)

O arquivo `.env` já existe com configuração padrão:

```
DATABASE_URL=postgresql://estoque_user:12345@localhost:5432/estoque_db
FLASK_ENV=production
SECRET_KEY=chave-super-secreta-mude-em-producao-b7x9kL2m5P9n3Q
```

**Para servidor remoto**, altere o IP:
```
DATABASE_URL=postgresql://estoque_user:12345@seu-ip-servidor:5432/estoque_db
```

---

## 🚀 Passo 3: Instalar Dependências (Já Feito!)

Todas as dependências já foram instaladas:
- ✓ Flask
- ✓ Flask-Login
- ✓ SQLAlchemy
- ✓ psycopg2-binary (PostgreSQL driver)
- ✓ python-dotenv

Se precisar reinstalar:
```bash
pip install -r requirements.txt
```

---

## ▶️ Passo 4: Iniciar o Sistema

### Servidor (máquina com PostgreSQL)

```bash
python app.py
```

Acesse: `http://localhost:5000`

### Clientes (outras máquinas)

```bash
python app.py
```

Acesse: `http://seu-ip-servidor:5000`

---

## 🔐 Login Padrão

**Usuário:** `admin`  
**Senha:** `admin`

⚠️ **Altere a senha após o primeiro acesso!**

---

## 📊 Informações que Aparecerão

Ao rodar `python app.py`, você verá:

```
============================================================
Sistema de Estoque - Inicializando...
============================================================
✓ Banco de dados: PostgreSQL
✓ URL: estoque_user@localhost:5432/estoque_db
============================================================

✓ Usuário admin criado (se for primeira vez)
✓ Banco de dados inicializado com sucesso
```

---

## 🧪 Testar Conexão

Para verificar se PostgreSQL está acessível:

```bash
psql -U estoque_user -h localhost -d estoque_db
```

Se conectar sem erros, está funcionando!

---

## ❌ Troubleshooting

### "FATAL: password authentication failed"
- Verifique a senha em `.env`
- A senha deve ser `12345` (ou a que você criou)

### "server is not running"
- PostgreSQL não está rodando
- Inicie o serviço PostgreSQL

### "ERROR: database 'estoque_db' does not exist"
- Crie o banco novamente (veja Passo 1)

### "Connection refused"
- Verifique o IP em `.env`
- Porta 5432 pode estar bloqueada (firewall)

---

## 🌐 Acesso pela Rede

Todas as máquinas acessarão o **mesmo banco de dados centralizadoPostgreSQL**!

1. Pegue IP do servidor: `ipconfig` (procure por IPv4 Address)
2. Altere `.env` em cada máquina com o IP correto
3. Todos acessarão os mesmos dados em tempo real ✓

---

## 📝 Próximos Passos

1. Execute: `python app.py`
2. Se houver erros, verifique a seção de Troubleshooting
3. Acesse: `http://localhost:5000` (ou seu IP)
4. Login com `admin` / `admin`
5. Altere a senha do admin
6. Comece a usar! 🎉
