import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "youshop.db"

def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto TEXT,
        visitas INTEGER,
        vendas INTEGER,
        preco REAL,
        origem TEXT 
    ) """)

    conn.commit()
    conn.close()

def salvar_analise(produto, visitas, vendas, preco, origem):
    """Salva uma nova análise no banco SQLite e retorna o ID do registro criado."""

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO analises
    (produto, visitas, vendas, preco, origem)
    VALUES (?, ?, ?, ?, ?)
    """, (produto, visitas, vendas, preco, origem))

    conn.commit()

    ultimo_id = cursor.lastrowid

    conn.close()

    return ultimo_id

def buscar_por_id(id):
    conn = conectar()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM analises WHERE id = ?", (id,)
    )

    resultado = cursor.fetchone()

    conn.close()

    return resultado

def buscar_todas():
    """Retorna todas as análises salvas, ordenadas da mais recente para a mais antiga."""

    conn = conectar()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM analises
    ORDER BY id DESC     
    """)

    resultados = cursor.fetchall()

    conn.close()

    return resultados