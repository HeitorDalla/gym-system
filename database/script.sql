-- =====================================================
-- SCRIPT MYSQL - SISTEMA DE ACADEMIA
-- =====================================================

CREATE DATABASE IF NOT EXISTS gym_system;
USE gym_system;

-- Configurações iniciais
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS treino_exercicios;
DROP TABLE IF EXISTS pagamento_clientes;
DROP TABLE IF EXISTS treinos;
DROP TABLE IF EXISTS clientes_academia;
DROP TABLE IF EXISTS exercicios;
DROP TABLE IF EXISTS instrutores;
DROP TABLE IF EXISTS planos;
SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- CRIAÇÃO DAS TABELAS
-- =====================================================

CREATE TABLE planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco_mensal DECIMAL(10,2) NOT NULL,
    duracao_meses INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE instrutores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE exercicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    grupo_muscular VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE clientes_academia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    idade INT NOT NULL CHECK (idade >= 16 AND idade <= 100),
    sexo ENUM('M', 'F', 'Outro') NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    plano_id INT NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Ativo', 'Inativo', 'Suspenso') DEFAULT 'Ativo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (plano_id) REFERENCES planos(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE treinos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    instrutor_id INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    plano_id INT NOT NULL,
    objetivo TEXT,
    observacoes TEXT,
    status ENUM('Ativo', 'Concluido', 'Cancelado') DEFAULT 'Ativo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes_academia(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (instrutor_id) REFERENCES instrutores(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (plano_id) REFERENCES planos(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CHECK (data_fim >= data_inicio)
);

CREATE TABLE treino_exercicios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    treino_id INT NOT NULL,
    exercicio_id INT NOT NULL,
    series VARCHAR(50) NOT NULL,
    repeticoes INT NOT NULL,
    carga DECIMAL(5,2),
    tempo_descanso INT COMMENT 'Tempo em segundos',
    observacoes TEXT,
    ordem_execucao INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (treino_id) REFERENCES treinos(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (exercicio_id) REFERENCES exercicios(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE KEY unique_treino_exercicio (treino_id, exercicio_id)
);

CREATE TABLE pagamento_clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    plano_id INT NOT NULL,
    valor_pago DECIMAL(10,2) NOT NULL,
    data_pagamento DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    forma_pagamento ENUM('Dinheiro', 'Cartão Débito', 'Cartão Crédito', 'PIX', 'Boleto') NOT NULL,
    status_pagamento ENUM('Pendente', 'Pago', 'Atrasado', 'Cancelado') DEFAULT 'Pendente',
    desconto DECIMAL(10,2) DEFAULT 0.00,
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes_academia(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (plano_id) REFERENCES planos(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- =====================================================
-- ÍNDICES PARA OTIMIZAÇÃO
-- =====================================================

CREATE INDEX idx_clientes_email ON clientes_academia(email);
CREATE INDEX idx_clientes_plano ON clientes_academia(plano_id);
CREATE INDEX idx_treinos_cliente ON treinos(cliente_id);
CREATE INDEX idx_treinos_instrutor ON treinos(instrutor_id);
CREATE INDEX idx_treinos_data ON treinos(data_inicio, data_fim);
CREATE INDEX idx_pagamentos_cliente ON pagamento_clientes(cliente_id);
CREATE INDEX idx_pagamentos_data ON pagamento_clientes(data_pagamento);
CREATE INDEX idx_exercicios_grupo ON exercicios(grupo_muscular);