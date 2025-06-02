import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
import sqlite3
import csv

# 📦 Conecta (ou cria) o banco de dados SQLite
conn = sqlite3.connect("gym-system.db", check_same_thread=False)
cursor = conn.cursor()

# Criação da tabela clientes (DDL)
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

# Criação da tabela instrutores (DDL)
cursor.execute('''
CREATE TABLE IF NOT EXISTS instrutores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especialidade TEXT NOT NULL
)
''')

# Criação da tabela planos (DDL)
cursor.execute('''
CREATE TABLE IF NOT EXISTS planos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco_mensal REAL NOT NULL,
    duracao_meses INTEGER NOT NULL
)
''')

# Criação da tabela exercicios (DDL)
cursor.execute('''
CREATE TABLE IF NOT EXISTS exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    grupo_muscular TEXT NOT NULL
)
''')

# Criação da tabela treinos (DDL)
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

# Criação da tabela treino_exercicio (DDL)
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

# Criação da tabela pagamentos (DDL)
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
conn.commit()


cursor.execute('PRAGMA foreign_keys = ON;')

df_exercicios = pd.read_csv('exercicios.csv')
df_exercicios.to_sql('exercicios', conn, if_exists='append', index=False)

df_exercicios = pd.read_csv('instrutores.csv')
df_exercicios.to_sql('instrutores', conn, if_exists='append', index=False)

df_exercicios = pd.read_csv('planos.csv')
df_exercicios.to_sql('planos', conn, if_exists='append', index=False)

df_exercicios = pd.read_csv('clientes_academia.csv')
df_exercicios.to_sql('clientes_academia', conn, if_exists='append', index=False)

df_exercicios = pd.read_csv('pagamento_clientes.csv')
df_exercicios.to_sql('pagamento_clientes', conn, if_exists='append', index=False)

df_exercicios = pd.read_csv('treinos.csv')
df_exercicios.to_sql('treinos', conn, if_exists='append', index=False)

df_exercicios = pd.read_csv('treino_exercicios.csv')
df_exercicios.to_sql('treino_exercicios', conn, if_exists='append', index=False)

    