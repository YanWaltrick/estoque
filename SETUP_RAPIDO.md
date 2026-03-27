# 🚀 SETUP RÁPIDO - Sistema de Estoque com MySQL

## ⚡ Começo Rápido (< 5 minutos)

### 1️⃣ Instalar Dependências + Configurar MySQL (Tudo Automático)

```bash
python setup_completo.py
```

Este script fará automaticamente:
- ✓ Instalar bibliotecas Python (Flask, SQLAlchemy, MySQL driver)
- ✓ Criar banco de dados no MySQL
- ✓ Criar usuário estoque_user
- ✓ Atualizar arquivo .env
- ✓ Testar conexão

### 2️⃣ Executar o Servidor

```bash
python app.py
```

Acesse no navegador:
```
http://localhost:5000
```

**Login padrão:**
- Usuário: `admin`
- Senha: `admin`

---

## 🛠️ Requisitos Prévios

### MySQL Community Server (obrigatório)

**Windows:**
1. Baixe: https://dev.mysql.com/downloads/mysql/
2. Execute o instalador
3. ✓ Marque "Add MySQL to PATH"
4. Anote a senha do usuário `root`
5. Conclua a instalação

**Verificar instalação:**
```bash
mysql --version
```

---

## 📋 O Que Cada Script Faz

| Script | Função |
|--------|--------|
| `setup_completo.py` | ⭐ **Use ESTE** - Faz tudo automaticamente |
| `instalar_dependencias.py` | Instala apenas Python packages |
| `configurar_mysql.py` | Configura apenas MySQL |
| `app.py` | Inicia o servidor Flask |

---

## 🔧 Configuração Manual (Se Preferir)

### Criar Banco Manualmente

Se `setup_completo.py` falhar, execute manualmente:

```bash
mysql -u root -p
```

Cole os comandos:

```sql
CREATE DATABASE IF NOT EXISTS estoque_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'estoque_user'@'%' IDENTIFIED BY '12345';
GRANT ALL PRIVILEGES ON estoque_db.* TO 'estoque_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

### Atualizar .env

Edite o arquivo `.env` na raiz do projeto:

```
DATABASE_URL=mysql+pymysql://estoque_user:12345@localhost:3306/estoque_db
FLASK_ENV=production
SECRET_KEY=chave-super-secreta-altere-em-producao-12345789
```

### Instalar Dependências Manualmente

```bash
pip install -r requirements.txt
```

---

## 📲 Para Acessar de Outras Máquinas

Se MySQL está em um servidor central:

1. Edite `.env` na máquina cliente:

```
DATABASE_URL=mysql+pymysql://estoque_user:12345@SEU-IP-SERVIDOR:3306/estoque_db
```

2. Execute o servidor:

```bash
python app.py
```

3. Acesse de qualquer máquina:

```
http://SEU-IP-SERVIDOR:5000
```

---

## ❌ Troubleshooting

### Erro: "mysql not found"
- MySQL não está instalado ou não está no PATH
- Instale: https://dev.mysql.com/downloads/mysql/
- Adicione ao PATH (reinicie o terminal depois)

### Erro: "Access denied"
- Senha incorreta do root
- Verifique em `configurar_mysql.py` qual senha você entrou

### Erro: "Can't connect to MySQL"
- MySQL não está rodando
- Windows: Inicie o serviço MySQL (Services)
- Linux: `sudo service mysql start`

### Erro: "Database 'estoque_db' doesn't exist"
- Execute o script de configuração novamente
- Ou crie manualmente (veja seção acima)

---

## 📊 Estrutura do Projeto

```
ESTOQUE/
├── app.py                    # 🚀 Servidor Flask principal
├── database.py               # ⚙️ Configuração do banco
├── models.py                 # 📦 Modelos SQLAlchemy
├── requirements.txt          # 📚 Dependências Python
├── .env                      # 🔐 Variáveis de ambiente
│
├── setup_completo.py         # ⭐ Setup automático (use isto!)
├── instalar_dependencias.py  # Instala python packages
├── configurar_mysql.py       # Configura MySQL
│
├── templates/                # 🎨 HTML do Frontend
│   ├── index.html
│   ├── login.html
│   └── admin.html
├── static/                   # 📁 CSS/JS
│   ├── css/
│   └── js/
└── iniciar_frontend.bat      # 🪟 Atalho Win
```

---

## 🎯 Resumo de Pucos

```
1. Verificá se MySQL está instalado
2. python setup_completo.py   ← Configura TUDO
3. python app.py              ← Inicia servidor
4. Abra http://localhost:5000 ← Acesse
5. Login: admin / admin       ← Entre
```

---

## 📞 Precisa de Ajuda?

- MySQL não inicia: Verifique Services (Windows) ou systemctl (Linux)
- Porta 5000 já em uso: `python app.py --port 8000`
- Quer resetar o banco: Delete arquivo estoque.db (SQlite) ou execute DROP DATABASE no MySQL

---

**Pronto? Execute:**

```bash
python setup_completo.py
```
