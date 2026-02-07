import sqlite3
import os

# Caminho absoluto do banco de dados
db_path = r"C:\Users\vancl\pdv\dist\pdv.db"

# Garante que a pasta existe
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Conectar ao banco (cria se não existir)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabela de usuários
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    sobrenome TEXT,
    login TEXT UNIQUE,
    senha TEXT
)
""")

# Tabela de produtos
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    descricao TEXT,
    quantidade REAL,
    tipo_quantidade TEXT,   -- Peso, Unidade, Caixa
    valor_compra REAL,
    estoque_minimo INTEGER,
    estoque_maximo INTEGER,
    valor_venda REAL
)
""")

# Tabela de vendas
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    quantidade REAL,
    valor_total REAL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(produto_id) REFERENCES produtos(id)
)
""")

# Tabela de financeiro
cursor.execute("""
CREATE TABLE IF NOT EXISTS financeiro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,              -- Entrada ou Saída
    descricao TEXT,
    valor REAL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Banco de dados criado com sucesso em:", db_path)
