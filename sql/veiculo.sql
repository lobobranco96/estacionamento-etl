CREATE TABLE IF NOT EXISTS veiculo (
    matricula INT NOT NULL,
    nome_funcionario VARCHAR(100),
    placa_veiculo VARCHAR(8),
    modelo_veiculo VARCHAR(30),
    cor VARCHAR(30),
    id_veiculo SERIAL PRIMARY KEY,
    id_funcionario SERIAL,
    FOREIGN KEY (id_funcionario) REFERENCES funcionario (id_funcionario)

);

