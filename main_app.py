import streamlit as st
from modules.database import initialize_database
from modules.auth import populate_usuarios, autenticar_usuario
from modules.queries import (get_clientes_planos, get_treinos_exercicios, get_nomes_clientes, 
                    get_pagamentos_cliente, get_nomes_instrutores, get_total_alunos_instrutor)
from modules.forms import (form_cadastro_cliente, form_cadastro_pagamento, 
                  form_cadastro_treino, form_cadastro_exercicio_treino)

# Inicializa o banco de dados
conn, cursor = initialize_database()

# Popula usuários se necessário
populate_usuarios(conn, cursor)

# =========================
# Interface do Streamlit
# =========================

# Controle de sessão
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = None

# Se não estiver logado, mostra tela de login
if not st.session_state.logado:
    st.title("Login de Usuário")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario = autenticar_usuario(cursor, email, senha)
        if usuario:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.success(f"Bem-vindo, {usuario[1]}!")
            st.rerun()
        else:
            st.error("Email ou senha incorretos. Tente novamente.")

# Se estiver logado, mostra conteúdo protegido
else:
    st.sidebar.success(f"Logado como: {st.session_state.usuario[1]}")

    st.title("🎓 Sistema para Academia")

    # 1 - Lista os clientes e seus planos
    st.subheader("Listagem dos clientes e seus planos")
    st.write('\n')

    df_clientesPlanos = get_clientes_planos(conn)
    st.dataframe(df_clientesPlanos)

    # 2 - Filtrar e mostrar treinos e seus exercícios
    df_treinosExercicios = get_treinos_exercicios(conn)
    st.dataframe(df_treinosExercicios)

    # 3 - Mostrar total de pagamentos e último pagamento por cliente
    st.subheader('Pagamentos por Clientes', divider=True)

    df_nomes_clientes = get_nomes_clientes(conn)

    nomes_clientes_dict = {
        f"{row['nome']} (ID {row['id']})": row['id']
        for _, row in df_nomes_clientes.iterrows()
    }

    cliente_selecionado = st.selectbox('Selecione um cliente:', options=list(nomes_clientes_dict.keys()))

    # Recupera o ID correspondente
    cliente_selecionado_id = nomes_clientes_dict[cliente_selecionado]

    total_pagamentos, ultimo_pagamento = get_pagamentos_cliente(cursor, cliente_selecionado_id)

    # Exibe os resultados na tela
    st.write(f'O cliente **{cliente_selecionado}** fez **{total_pagamentos}** pagamentos.')

    if ultimo_pagamento:
        valor, data = ultimo_pagamento
        st.write(f'Seu último pagamento foi de **R$ {valor:.2f}**, em **{data}**.')
    else:
        st.write('Ainda não há pagamentos registrados para este cliente.')

    # 4 - Quantidade de clientes por instrutor
    st.subheader('Quantidade de Clientes por Instrutor', divider=True)

    df_nomes_instrutor = get_nomes_instrutores(conn)

    nomes_instrutor_dict = {
        f"{row['nome']} (ID {row['id']})": row['id']
        for _, row in df_nomes_instrutor.iterrows()
    }

    instrutor_selecionado = st.selectbox('Selecione um instrutor:', options=list(nomes_instrutor_dict.keys()))

    instrutor_selecionado_id = nomes_instrutor_dict[instrutor_selecionado]

    total_alunos = get_total_alunos_instrutor(cursor, instrutor_selecionado_id)

    st.write(f'O instrutor **{instrutor_selecionado}** possui **{total_alunos}** alunos.')

    # Formulários para cadastro
    st.subheader("Cadastros", divider='grey')
    opcao_menu = st.selectbox('Escolha uma opção para cadastrar', ['Cliente', 'Pagamento', 'Treino', 'Exercicios por Treino'])

    if opcao_menu == 'Cliente':
        form_cadastro_cliente(conn, cursor)
    elif opcao_menu == 'Pagamento':
        form_cadastro_pagamento(conn, cursor)
    elif opcao_menu == 'Treino':
        form_cadastro_treino(conn, cursor)
    elif opcao_menu == 'Exercicios por Treino':
        form_cadastro_exercicio_treino(conn, cursor)

    st.write('\n')
    st.write('\n')

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.session_state.usuario = None
        st.rerun()