CREATE VIEW estacionamento AS
SELECT 
    f.matricula, 
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(f.nome_funcionario, 'Sr.', ''),
                        'Sra.', ''),
                    'Dr.', ''),
                'Srta.', ''),
            'Dra.', '') AS nome_funcionario, 
    f.nivel_hierarquico, 
    v.placa_veiculo, 
    v.modelo_veiculo, 
    v.cor,
    CASE 
        WHEN f.nivel_hierarquico = 'Diretor' THEN 'Todos os estacionamentos'
        WHEN f.nivel_hierarquico = 'Equipe' THEN 'Lq303 e divina'
        WHEN f.nivel_hierarquico = 'Equipe Técnico Operacional' THEN 'Nenhum estacionamento'
        WHEN f.nivel_hierarquico = 'Gerente' THEN 'Divina e 695'
        WHEN f.nivel_hierarquico = 'Gerente Sr' THEN 'Divina, 70 e 695'
        WHEN f.nivel_hierarquico = 'Supervisor' THEN 'Lq303 e divina'
        WHEN f.nivel_hierarquico = 'Especialista' THEN 'Todos os estacionamentos'
    END AS elegibilidade_estacionamento,
    regiao,
        CASE 
            WHEN substr(REPLACE(REPLACE(f.telefone, '(', ''), ')', ''), 1, 1) = '0' 
                THEN CONCAT('+55 ', substr(REPLACE(REPLACE(REPLACE(telefone, '(', ''), ')', ''), '-', ' '), 2))
            WHEN length(f.telefone) = 12 
                THEN CONCAT('+55 ', REPLACE(REPLACE(REPLACE(f.telefone, '-', ' '), '(', ''), ')', ''))
            ELSE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(f.telefone, '-', ' '), '(0', ''), ')', ' 9'), '(', ''), ')', '')
        END AS telefone,
        REPLACE(
            REPLACE(
                REPLACE(f.email, '@example.org', '@hotmail.com'),
                '@example.com', '@gmail.com'),
            '@example.net', '@yahoo.com.br') AS email
FROM funcionario f
JOIN veiculo v ON f.matricula = v.matricula;