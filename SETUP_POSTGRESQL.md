# Guia Rápido - Sistema de Estoque com MySQL

## Passo 1: Instalação do MySQL

### Windows

1. **Baixar:**
   - Acesse: https://dev.mysql.com/downloads/mysql/
      - Selecione a versão mais recente (recomendo 8.x)
      
2. **Instalar:**
   - Execute o instalador
      - Marque a opção para adicionar ao PATH
         - Anote a senha do usuário `root`
            - Porta padrão: `3306`
            
3. **Verificar instalação:**
   ```bash
      mysql --version
         ```
         
---

## Passo 2: Criar Banco de Dados

No MySQL, execute em terminal:
   
   ```bash
   mysql -u root -p
   # Digite a senha do root
   
CREATE DATABASE IF NOT EXISTS estoque_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'estoque_user'@'%' IDENTIFIED BY '12345';
GRANT ALL PRIVILEGES ON estoque_db.* TO 'estoque_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

---

## Passo 3: Configurar Variáveis de Ambiente

Crie/edite `.env` no projeto:
   
   ```
   DATABASE_URL=mysql+pymysql://estoque_user:12345@localhost:3306/estoque_db
   FLASK_ENV=production
   SECRET_KEY=sua-chave-secreta-muito-segura-aqui
   ```
   
---

## Passo 4: Instalar Dependências Python

```bash
python -m pip install -r requirements.txt
```

---

## Passo 5: Iniciar Sistema

```bash
python app.py
```

Acesse: `http://localhost:5000`

---

## Verificação

```bash
mysql -u estoque_user -p -h localhost -D estoque_db
```

---

## Troubleshooting

- "Connection refused" => MySQL não está rodando / firewall na porta 3306
- "Access denied" => usuário/senha errados em `.env`
- "Unknown database" => banco `estoque_db` não foi criado
