import hashlib

def hash_senha(senha):
    """Gera hash da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

def populate_usuarios(conn, cursor):
    """Popula a tabela com 5 usuários, se estiver vazia"""
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        usuarios = [
            ("Alice Santos", "alice@email.com", "senha123"),
            ("Bruno Silva", "bruno@email.com", "segredo"),
            ("Carlos Lima", "carlos@email.com", "academia"),
            ("Diana Costa", "diana@email.com", "fitness"),
            ("Eduarda Reis", "eduarda@email.com", "malhacao")
        ]
        for nome, email, senha in usuarios:
            senha_hash = hash_senha(senha)
            cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
                            (nome, email, senha_hash))
        conn.commit()

def autenticar_usuario(cursor, email, senha):
    """Autentica o usuário pelo email e senha (com hash)"""
    senha_hash = hash_senha(senha)
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha_hash))
    return cursor.fetchone()