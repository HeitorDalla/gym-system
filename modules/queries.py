import pandas as pd

def get_clientes_planos(conn):
    # Lista os clientes e seus planos
    df_clientesPlanos = pd.read_sql_query('''
        select
            c.nome as `Nome do cliente`,
            p.nome as `Plano`
        from clientes_academia as c
        left join planos p on c.plano_id = p.id
    ''', conn)

    return df_clientesPlanos

def get_treinos_exercicios(conn):
    # Filtrar e mostrar treinos e seus exercícios
    df_treinosExercicios = pd.read_sql_query('''
        select
            t.id as `Treino`,
            group_concat(e.nome, ', ') as `Exercicio`
        from treinos t
        inner join treino_exercicios te on te.treino_id = t.id
        inner join exercicios e on te.exercicio_id = e.id
        group by t.id
    ''', conn)

    return df_treinosExercicios

def get_nomes_clientes(conn):
    # Retorna lista de clientes
    df_nomes_clientes = pd.read_sql('''
        SELECT id, nome FROM clientes_academia
    ''', conn)

    return df_nomes_clientes

def get_pagamentos_cliente(cursor, cliente_id):
    # Busca informações de pagamento de um cliente específico

    # Conta quantos pagamentos esse cliente já fez
    cursor.execute('SELECT COUNT(*) FROM pagamento_clientes WHERE cliente_id = ?', (cliente_id,))
    total_pagamentos = cursor.fetchone()[0]

    # Busca o último pagamento (valor e data), ordenando pela data
    cursor.execute('''
        SELECT valor_pago, data_pagamento
        FROM pagamento_clientes
        WHERE cliente_id = ?
        ORDER BY data_pagamento DESC
        LIMIT 1
    ''', (cliente_id,))

    ultimo_pagamento = cursor.fetchone()
    
    return total_pagamentos, ultimo_pagamento

def get_nomes_instrutores(conn):
    # Retorna lista de instrutores
    df_nomes_instrutor = pd.read_sql_query('''
        SELECT id, nome FROM instrutores
    ''', conn)

    return df_nomes_instrutor

def get_total_alunos_instrutor(cursor, instrutor_id):
    # Retorna quantidade de alunos de um instrutor
    cursor.execute(
        '''
        SELECT COUNT(DISTINCT cliente_id)
        FROM treinos
        WHERE instrutor_id = ?
    ''', (instrutor_id,)
    )

    total_alunos = cursor.fetchone()[0]
    
    return total_alunos