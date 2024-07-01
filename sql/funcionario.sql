CREATE TABLE IF NOT EXISTS funcionario (
    matricula INT NOT NULL,
    nome_funcionario VARCHAR(100),
    cargo VARCHAR(100),
    nivel_hierarquico VARCHAR(50),
    regiao CHAR(3),
    email VARCHAR(255),
    telefone VARCHAR(30),
    id_funcionario SERIAL PRIMARY KEY
);




