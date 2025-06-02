import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
import sqlite3
import csv

# 📦 Conecta (ou cria) o banco de dados SQLite
conn = sqlite3.connect("database/gym-system.db", check_same_thread=False)
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


# 3. Criar uma aplicação Streamlit para:
# 	3.1. Listar clientes e seus planos;
# 	3.2. Filtrar e mostrar treinos e seus exercícios;
# 	3.3. Mostrar total de pagamentos e último pagamento por cliente;
# 	3.4. Mostrar quantos clientes cada instrutor atende;
# 	3.5. Formulário para cadastro de clientes, pagamentos, treinos e exercícios nos treinos;
# 	3.6. EXTRA: Usar a função de autenticação do streamlit para criar um login e senha.


# 1 - Lista os clientes e seus planos
st.subheader("Listagem dos clientes e seus planos")
st.write('\n')

df_clientesPlanos = pd.read_sql_query('''
    select
        c.nome as `Nome do cliente`,
        p.nome as `Plano`
    from clientes_academia as c
    left join planos p on c.plano_id = p.id
''', conn)
st.dataframe(df_clientesPlanos)


# 2 - Filtrar e mostrar treinos e seus exercícios
df_treinosExercicios = pd.read_sql_query('''
    select
        t.id as `Treino`,
        group_concat(e.nome, ', ') as `Exercicio`
    from treinos t
    inner join treino_exercicios te on te.treino_id = t.id
    inner join exercicios e on te.exercicio_id = e.id
    group by t.id
''', conn)
st.dataframe(df_treinosExercicios)


# 3 - Mostrar total de pagamentos e último pagamento por cliente
st.subheader('Pagamentos por Clientes', divider=True)

df_nomes_clientes = pd.read_sql('''
	SELECT id, nome FROM clientes_academia
''', conn)

nomes_clientes_dict = {
    f"{row['nome']} (ID {row['id']})": row['id']
    for _, row in df_nomes_clientes.iterrows()
}

cliente_selecionado = st.selectbox('Selecione um cliente:', options=list(nomes_clientes_dict.keys()))

# Recupera o ID correspondente
cliente_selecionado_id = nomes_clientes_dict[cliente_selecionado]

# Conta quantos pagamentos esse cliente já fez
cursor.execute('SELECT COUNT(*) FROM pagamento_clientes WHERE cliente_id = ?', (cliente_selecionado_id,))
total_pagamentos = cursor.fetchone()[0]

# Busca o último pagamento (valor e data), ordenando pela data
cursor.execute('''
    SELECT valor_pago, data_pagamento
    FROM pagamento_clientes
    WHERE cliente_id = ?
    ORDER BY data_pagamento DESC
    LIMIT 1
''', (cliente_selecionado_id,))
ultimo_pagamento = cursor.fetchone()

# Exibe os resultados na tela
st.write(f'O cliente **{cliente_selecionado}** fez **{total_pagamentos}** pagamentos.')

if ultimo_pagamento:
    valor, data = ultimo_pagamento
    st.write(f'Seu último pagamento foi de **R$ {valor:.2f}**, em **{data}**.')
else:
    st.write('Ainda não há pagamentos registrados para este cliente.')


# 4 - Quantidade de clientes por instrutor
st.subheader('Quantidade de Clientes por Instrutor', divider=True)

df_nomes_instrutor = pd.read_sql_query('''
    SELECT id, nome FROM instrutores
''', conn)

nomes_instrutor_dict = {
    f"{row['nome']} (ID {row['id']})": row['id']
    for _, row in df_nomes_instrutor.iterrows()
}

instrutor_selecionado = st.selectbox('Selecione um instrutor:', options=list(nomes_instrutor_dict.keys()))

instrutor_selecionado_id = nomes_instrutor_dict[instrutor_selecionado]

cursor.execute(
    '''
    SELECT COUNT(DISTINCT cliente_id)
    FROM treinos
    WHERE instrutor_id = ?
''', (instrutor_selecionado_id,)
)
total_alunos = cursor.fetchone()[0]

st.write(f'O instrutor **{instrutor_selecionado}** possui **{total_alunos}** alunos.')


# Formulários para cadastro de clientes, pagamentos, treinos e exercícios nos treinos
st.title("🎓 Sistema para Academia")

st.subheader("Fazer Novo Cadastro", divider='grey')
opcao_menu = st.selectbox('Escolha uma opção para cadastrar', ['Cliente', 'Pagamento', 'Treino', 'Exercicios por Treino'])

if opcao_menu == 'Cliente':
    st.write('Cliente')

    with st.form("form_cliente", clear_on_submit=True):
        nome_cliente = st.text_input("Nome Cliente")
        idade_cliente = st.text_input("Idade Cliente")
        sexo_cliente = st.text_input("Sexo Cliente(M/F)")
        email_cliente = st.text_input("E-mail Cliente")
        telefone_cliente = st.text_input("Telefone Cliente")
        menu_planos = pd.read_sql_query("SELECT * FROM planos ORDER BY id ASC", conn)
        plano = st.selectbox("Planos", menu_planos["nome"])
        cadastrar = st.form_submit_button("Cadastrar")

    if cadastrar:
            plano_id = int(menu_planos[menu_planos["nome"] == plano]["id"].values[0])
            cursor.execute('''
                           INSERT INTO clientes_academia 
                           (nome, idade, sexo, email, telefone, plano_id) VALUES (?, ?, ?, ?, ?, ?)
                        ''',(nome_cliente, idade_cliente, sexo_cliente, email_cliente, telefone_cliente, plano_id)
                        )
            
            conn.commit()
            st.success(f"Cadastro feito com sucesso")

elif opcao_menu == 'Pagamento':
    st.write('Pagamento')

    menu_cliente = pd.read_sql_query("SELECT * FROM clientes_academia ORDER BY nome ASC", conn)
    menu_planos = pd.read_sql_query("SELECT * FROM clientes_academia ORDER BY nome ASC", conn)

    with st.form("form_pagamento", clear_on_submit=True):
        clientes_opcao = ["-- Selecione o Cliente --"] + menu_cliente["nome"].tolist()
        nome_cliente = st.selectbox("Selecione o Cliente para Pagamento", clientes_opcao)
        pagar = st.form_submit_button("Pago")

        if pagar:
            if (nome_cliente != '-- Selecione o Cliente --'):
                id_cliente = int(menu_cliente[menu_cliente["nome"] == nome_cliente]["id"].values[0])
                id_plano_cliente = int(menu_cliente[menu_cliente["nome"] == nome_cliente]["plano_id"].values[0])
                data_pagamento = datetime.now().strftime("%Y-%m-%d")
                df_valor_plano = pd.read_sql_query("SELECT preco_mensal FROM planos WHERE id = ?", conn, params=(id_plano_cliente,))
                preco_plano = df_valor_plano['preco_mensal'].iloc[0]
                cursor.execute("INSERT INTO pagamento_clientes (cliente_id, plano_id, valor_pago, data_pagamento) VALUES (?, ?, ?, ?)",
                    (id_cliente, id_plano_cliente, preco_plano, data_pagamento))
                conn.commit()
                st.success(f"Pagamento feito com sucesso")
            else:
                st.error(f"Favor selecionar um cliente.")

elif opcao_menu == 'Treino':
    st.write('Treino')

    df_clientes = pd.read_sql_query("select * from clientes_academia order by nome", conn)
    df_instrutor = pd.read_sql_query("select * from instrutores order by nome", conn)
    df_planos = pd.read_sql_query("select * from planos order by nome", conn)
    
    with st.form('Formulário para cadastro de treinos', clear_on_submit=True):
        nome_cliente = st.selectbox("Nome cliente", df_clientes['nome'])
        nome_instrutor = st.selectbox("Nome instrutor", df_instrutor['nome'])
        data_inicio = st.text_input("Data de início [DD/MM/AAAA]")
        data_fim = st.text_input("Data do fim [DD/MM/AAAA]")
        plano_escolhido = st.selectbox("Planos", df_planos['nome'])

        button = st.form_submit_button("Cadastrar")

        if button:
            if nome_cliente and nome_instrutor and data_inicio and data_fim and plano_escolhido:
                # Recuperar os ids do clientes e instrutores
                id_nome = int(df_clientes[df_clientes['nome'] == nome_cliente]['id'].values[0])
                id_instrutor = int(df_instrutor[df_instrutor['nome'] == nome_instrutor]['id'].values[0])
                id_plano = int(df_planos[df_planos['nome'] == plano_escolhido]['id'].values[0])

                cursor.execute('''
                    insert into treinos
                    (cliente_id, instrutor_id, data_inicio, data_fim, plano_id)
                    values (?, ?, ?, ?, ?)
                ''', ((id_nome, id_instrutor, data_inicio, data_fim, id_plano)))

                conn.commit()
                st.success("Treino cadastrado com sucesso!")