import sqlite3
import pandas as pd

def get_connection():
    """Conecta (ou cria) o banco de dados SQLite"""
    
    conn = sqlite3.connect("database/gym-system.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    return conn, cursor

def create_tables(conn, cursor):
    """Criação de todas as tabelas necessárias"""
    
    # Criação da tabela clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes_academia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        sexo TEXT NOT NULL,
        email TEXT NOT NULL,
        telefone TEXT NOT NULL,
        plano_id INTEGER NOT NULL,
        FOREIGN KEY(plano_id) REFERENCES planos(id)
    )
    ''')

    # Criação da tabela instrutores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS instrutores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        especialidade TEXT NOT NULL
    )
    ''')

    # Criação da tabela planos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS planos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco_mensal REAL NOT NULL,
        duracao_meses INTEGER NOT NULL
    )
    ''')

    # Criação da tabela exercicios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS exercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        grupo_muscular TEXT NOT NULL
    )
    ''')

    # Criação da tabela treinos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS treinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        instrutor_id INTEGER NOT NULL,
        data_inicio TEXT NOT NULL,
        data_fim TEXT NOT NULL,
        plano_id INTEGER NOT NULL,
        FOREIGN KEY(cliente_id) REFERENCES clientes_academia(id),
        FOREIGN KEY(instrutor_id) REFERENCES instrutores(id),
        FOREIGN KEY(plano_id) REFERENCES planos(id)
    )
    ''')

    # Criação da tabela treino_exercicio
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS treino_exercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        treino_id INTEGER NOT NULL,
        exercicio_id INTEGER NOT NULL,
        series TEXT NOT NULL,
        repeticoes INTEGER NOT NULL,
        FOREIGN KEY(treino_id) REFERENCES treinos(id),
        FOREIGN KEY(exercicio_id) REFERENCES exercicios(id)
    )
    ''')

    # Criação da tabela pagamentos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagamento_clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER NOT NULL,
        plano_id INTEGER NOT NULL,
        valor_pago REAL NOT NULL,
        data_pagamento TEXT NOT NULL,
        FOREIGN KEY(cliente_id) REFERENCES clientes_academia(id),
        FOREIGN KEY(plano_id) REFERENCES planos(id)
    )
    ''')

    # Criação da tabela usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    
    conn.commit()

def populate_tables(conn, cursor):
    """Popula as tabelas com dados dos CSVs se estiverem vazias"""
    
    cursor.execute("SELECT COUNT(*) FROM exercicios")
    if cursor.fetchone()[0] == 0:
        df_exercicios = pd.read_csv('csv/exercicios.csv')
        df_exercicios.to_sql('exercicios', conn, if_exists='append', index=False)

    cursor.execute("SELECT COUNT(*) FROM instrutores")
    if cursor.fetchone()[0] == 0:
        df_exercicios = pd.read_csv('csv/instrutores.csv')
        df_exercicios.to_sql('instrutores', conn, if_exists='append', index=False)

    cursor.execute("SELECT COUNT(*) FROM planos")
    if cursor.fetchone()[0] == 0:
        df_exercicios = pd.read_csv('csv/planos.csv')
        df_exercicios.to_sql('planos', conn, if_exists='append', index=False)

    cursor.execute("SELECT COUNT(*) FROM clientes_academia")
    if cursor.fetchone()[0] == 0:
        df_exercicios = pd.read_csv('csv/clientes_academia.csv')
        df_exercicios.to_sql('clientes_academia', conn, if_exists='append', index=False)

    cursor.execute("SELECT COUNT(*) FROM pagamento_clientes")
    if cursor.fetchone()[0] == 0:
        df_exercicios = pd.read_csv('csv/pagamento_clientes.csv')
        df_exercicios.to_sql('pagamento_clientes', conn, if_exists='append', index=False)

    cursor.execute("SELECT COUNT(*) FROM treinos")
    if cursor.fetchone()[0] == 0:
        df_exercicios = pd.read_csv('csv/treinos.csv')
        df_exercicios.to_sql('treinos', conn, if_exists='append', index=False)

    cursor.execute("SELECT COUNT(*) FROM treino_exercicios")
    if cursor.fetchone()[0] == 0:
        df_exercicios = pd.read_csv('csv/treino_exercicios.csv')
        df_exercicios.to_sql('treino_exercicios', conn, if_exists='append', index=False)

def initialize_database():
    """Inicializa o banco de dados completo"""

    conn, cursor = get_connection()
    create_tables(conn, cursor)
    populate_tables(conn, cursor)
    return conn, cursor