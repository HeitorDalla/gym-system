import streamlit as st
import pandas as pd
from datetime import datetime

def form_cadastro_cliente(conn, cursor):
    """Formulário para cadastro de cliente"""
    st.write('Cliente')

    menu_planos = pd.read_sql_query("SELECT * FROM planos ORDER BY id ASC", conn)

    with st.form("form_cliente", clear_on_submit=True):
        nome_cliente = st.text_input("Nome Cliente")
        idade_cliente = st.text_input("Idade Cliente")
        sexo_cliente = st.text_input("Sexo Cliente(M/F)")
        email_cliente = st.text_input("E-mail Cliente")
        telefone_cliente = st.text_input("Telefone Cliente")
        plano = st.selectbox("Planos", menu_planos["nome"])

        cadastrar = st.form_submit_button("Cadastrar")

    if cadastrar:
        if  nome_cliente and idade_cliente and sexo_cliente and email_cliente and telefone_cliente:
            cursor.execute("SELECT COUNT(*) FROM clientes_academia WHERE nome = ?", (nome_cliente,)) #Verifica se o cliente ja existe
            
            if cursor.fetchone()[0] == 0:
                plano_id = int(menu_planos[menu_planos["nome"] == plano]["id"].values[0])

                cursor.execute('''
                    INSERT INTO clientes_academia 
                    (nome, idade, sexo, email, telefone, plano_id) VALUES (?, ?, ?, ?, ?, ?)
                ''', (nome_cliente, idade_cliente, sexo_cliente, email_cliente, telefone_cliente, plano_id))
                
                conn.commit()
                st.success(f"Cadastro feito com sucesso")
            else:
                st.error(f'Cliente ja existe!')
        else:
            st.error(f'Favor preencher todos os campos!')

def form_cadastro_pagamento(conn, cursor):
    """Formulário para cadastro de pagamento"""
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

                cursor.execute('''
                    INSERT INTO pagamento_clientes
                    (cliente_id, plano_id, valor_pago, data_pagamento)
                    VALUES (?, ?, ?, ?)
                ''', (id_cliente, id_plano_cliente, preco_plano, data_pagamento))
                
                conn.commit()
                st.success(f"Pagamento feito com sucesso")
            else:
                st.error(f"Favor selecionar um cliente.")

def form_cadastro_treino(conn, cursor):
    """Formulário para cadastro de treino"""
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

def form_cadastro_exercicio_treino(conn, cursor):
    """Formulário para cadastro de exercícios por treino"""
    st.write('Exercicios por Treino')

    menu_treino = pd.read_sql_query("SELECT * FROM treinos", conn)
    menu_exercicio = pd.read_sql_query("SELECT * FROM exercicios", conn)

    with st.form("form_novo_exercicio_treino", clear_on_submit=True):
        numero_treino = st.selectbox("Treino", menu_treino["id"])
        nome_exercicio = st.selectbox("Exercicio", menu_exercicio["nome"])
        qtd_serie = st.text_input("Quantidade de Séries")
        qtd_repeticoes = st.text_input("Quantidade de Repetições")

        cadastrar_exercicio = st.form_submit_button("Cadastrar")

        if cadastrar_exercicio:
            treino_id = int(menu_treino[menu_treino["id"] == numero_treino]["id"].values[0])
            id_exercicio = int(menu_exercicio[menu_exercicio["nome"] == nome_exercicio]["id"].values[0])

            cursor.execute('''
                INSERT INTO treino_exercicios
                (treino_id, exercicio_id, series, repeticoes) 
                VALUES(?, ?, ?, ?)
            ''', (treino_id, id_exercicio, qtd_serie,qtd_repeticoes))
            
            conn.commit()
            st.success(f"Exericio {nome_exercicio} cadastrado com sucesso para o treino {treino_id}!")