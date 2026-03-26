# Configuração PostgreSQL - Sistema de Estoque

## Passo 1: Instalação do PostgreSQL

### Windows

1. **Baixar:**
   - Acesse: https://www.postgresql.org/download/windows/
   - Clique em "Download the installer"
   - Selecione a versão mais recente (recomendo 15+)

2. **Instalar:**
   - Execute o instalador
   - Anote a senha do usuário `postgres` (você precisará dela)
   - Porta padrão: `5432`
   - Deixe todos os componentes selecionados

3. **Verificar instalação:**
   ```bash
   psql --version
   ```

---

## Passo 2: Criar Banco de Dados

Após instalar PostgreSQL, execute no PowerShell:

```bash
# Conectar ao PostgreSQL (solicitará senha do postgres)
psql -U postgres

# Dentro do psql, execute:
CREATE USER estoque_user WITH PASSWORD 'sua_senha_segura';
CREATE DATABASE estoque_db OWNER estoque_user;
GRANT ALL PRIVILEGES ON DATABASE estoque_db TO estoque_user;
\q
```

**Exemplo:**
```bash
psql -U postgres
CREATE USER estoque_user WITH PASSWORD '12345';
CREATE DATABASE estoque_db OWNER estoque_user;
GRANT ALL PRIVILEGES ON DATABASE estoque_db TO estoque_user;
\q
```

---

## Passo 3: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na pasta do projeto (mesmo nível do `app.py`):

```
DATABASE_URL=postgresql://estoque_user:sua_senha_segura@seu-ip-servidor:5432/estoque_db
FLASK_ENV=production
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
```

**Exemplo:**
```
DATABASE_URL=postgresql://estoque_user:12345@192.168.1.100:5432/estoque_db
FLASK_ENV=production
SECRET_KEY=MinhaChaveSuperSecretaB7x9kL2m5P
```

---

## Passo 4: Instalar Dependências Python

Instale o driver PostgreSQL:

```bash
python -m pip install -r requirements.txt
```

(O `psycopg2-binary` será adicionado ao requirements.txt automaticamente)

---

## Passo 5: Iniciando o Sistema

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

## Verificação

Verifique a conexão com:

```bash
psql -U estoque_user -h seu-ip-servidor -d estoque_db
```

Se conectou com sucesso, está funcionando!

---

## Troubleshooting

### "Connection refused"
- PostgreSQL não está rodando
- Verifique o IP do servidor
- Porta 5432 pode estar bloqueada no firewall

### "Invalid password"
- Verifique a senha no arquivo `.env`
- Senha no `.env` deve corresponder à criar no banco

### "Database não existe"
- Execute novamente os comandos CREATE DATABASE

---

## Próximas Etapas Automáticas

Após o PostgreSQL estar configurado e rodando:
1. Volte ao VS Code
2. Diga "postgres configurado"
3. Vou atualizar o código automaticamente para usar PostgreSQL
