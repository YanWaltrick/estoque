-- ============================================
-- SCHEMA PARA BANCO DE DADOS SQL (FUTURO)
-- ============================================
-- Este arquivo contém a estrutura SQL se você
-- quiser migrar para um banco de dados robusto
-- 
-- Compatível com: SQLite, MySQL, PostgreSQL

-- ============================================
-- TABELA: produtos
-- ============================================
CREATE TABLE produtos (
    id_produto VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    preco DECIMAL(10, 2) NOT NULL,
    quantidade INT NOT NULL DEFAULT 0,
    minimo INT NOT NULL DEFAULT 0,
    localizacao VARCHAR(255),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABELA: movimentacoes (histórico)
-- ============================================
CREATE TABLE movimentacoes (
    id_movimentacao INT AUTO_INCREMENT PRIMARY KEY,
    id_produto VARCHAR(50) NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('ENTRADA', 'SAIDA')),
    quantidade INT NOT NULL,
    motivo VARCHAR(255),
    data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(100),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

-- ============================================
-- TABELA: categorias
-- ============================================
CREATE TABLE categorias (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    descricao VARCHAR(255),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABELA: usuarios (para autenticação futura)
-- ============================================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- TABELA: auditorias (para registrar mudanças)
-- ============================================
CREATE TABLE auditorias (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    acao VARCHAR(255) NOT NULL,
    tabela VARCHAR(100),
    registro_id VARCHAR(50),
    dados_antigos JSON,
    dados_novos JSON,
    data_auditoria DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- ============================================
-- ÍNDICES PARA OTIMIZAÇÃO
-- ============================================

CREATE INDEX idx_categoria ON produtos(categoria);
CREATE INDEX idx_quantidade_baixa ON produtos(quantidade);
CREATE INDEX idx_id_produto_mov ON movimentacoes(id_produto);
CREATE INDEX idx_data_mov ON movimentacoes(data_movimentacao);

-- ============================================
-- CONSULTAS ÚTEIS
-- ============================================

-- Produtos com estoque baixo
SELECT * FROM produtos 
WHERE quantidade < minimo 
ORDER BY categoria, nome;

-- Valor total do estoque
SELECT 
    SUM(quantidade * preco) as valor_total,
    COUNT(*) as total_produtos,
    SUM(quantidade) as total_unidades
FROM produtos;

-- Produtos por categoria
SELECT 
    categoria,
    COUNT(*) as Total_Produtos,
    SUM(quantidade) as Total_Unidades,
    SUM(quantidade * preco) as Valor_Total
FROM produtos
GROUP BY categoria
ORDER BY Valor_Total DESC;

-- Histórico de movimentações
SELECT 
    p.nome,
    m.tipo,
    m.quantidade,
    m.data_movimentacao,
    m.motivo
FROM movimentacoes m
JOIN produtos p ON m.id_produto = p.id_produto
ORDER BY m.data_movimentacao DESC
LIMIT 100;

-- ============================================
-- FUNÇÃO: Atualizar data de modificação
-- ============================================

CREATE TRIGGER atualizar_data_produtos
BEFORE UPDATE ON produtos
FOR EACH ROW
SET NEW.data_atualizacao = CURRENT_TIMESTAMP;

-- ============================================
-- FUNÇÃO: Registrar movimentação
-- ============================================

CREATE TRIGGER registrar_entrada
AFTER INSERT ON movimentacoes
FOR EACH ROW
BEGIN
    IF NEW.tipo = 'ENTRADA' THEN
        UPDATE produtos SET quantidade = quantidade + NEW.quantidade
        WHERE id_produto = NEW.id_produto;
    ELSEIF NEW.tipo = 'SAIDA' THEN
        UPDATE produtos SET quantidade = quantidade - NEW.quantidade
        WHERE id_produto = NEW.id_produto;
    END IF;
END;

-- ============================================
-- NOTA IMPORTANTE
-- ============================================
/*
Este schema está disponível para quando você
quiser expandir o sistema para um banco de dados
robusto como MySQL ou PostgreSQL.

Para usar:
1. Crie um novo banco: CREATE DATABASE estoque_db;
2. Execute os comandos CREATE TABLE acima
3. Modifique estoque.py para conectar ao BD
4. Migre os dados do JSON

Benefícios:
- Suporte para múltiplos usuários
- Segurança melhorada
- Histórico completo
- Queries avançadas
- Escalabilidade

Veja em: estoque_expandido_sql.py (futuro)
*/
