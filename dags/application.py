from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.dates import days_ago
from airflow.decorators import task_group
import requests
import pandas as pd
import tempfile
from datetime import datetime


default_args = {
    'owner': 'github.com/lobobranco96',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

"""
Este DAG do Airflow realiza o processo de Extração, Transformação e Carga (EL e ETL) de dados
utilizando uma aplicação Flask hospedada em um container Docker. A aplicação Flask expõe um endpoint REST
que gera informações fictícias sobre funcionários e veículos brasileiros.

Os dados extraídos do endpoint são então inseridos nas tabelas correspondentes ('funcionario' e 'veiculo')
em um banco de dados PostgreSQL hospedado no serviço RDS da AWS.

Funcionamento do DAG:

1. Criação das Tabelas:
   - Define duas tarefas que criam as tabelas 'funcionario' e 'veiculo' no banco de dados PostgreSQL.
   - Utiliza o operador PostgresOperator do Airflow para executar SQL para criação das tabelas.

2. Extração de Dados:
   - Usa um PythonOperator para chamar a função 'extrair_dados_do_endpoint', que faz uma requisição GET para
     o endpoint da aplicação Flask.
   - Os dados são extraídos do JSON de resposta e armazenados temporariamente no XCom do Airflow.

3. Inserção de Dados:
   - Um task group ('inserir_para_db') é definido para agrupar as tarefas de inserção de dados.
   - Duas tarefas PythonOperator inserem os dados extraídos (funcionários e veículos) nas respectivas tabelas
     do banco de dados PostgreSQL.
   - Utiliza o PostgresHook para inserção em lote, garantindo eficiência na carga de dados.

Configuração Adicional:
- O DAG é configurado para iniciar diariamente ('@daily') desde um dia antes da data atual.
- Usa conexões e variáveis do Airflow para configurar a conexão com o banco de dados PostgreSQL ('postgres_conn').

Pré-requisitos:
- A aplicação Flask deve estar em execução e acessível na URL específica.
- O serviço RDS da AWS com PostgreSQL deve estar configurado e acessível pelo Airflow.

Este DAG permite automatizar o processo de atualização contínua de dados fictícios de funcionários e veículos
no banco de dados PostgreSQL, facilitando o desenvolvimento e testes de aplicações que dependem desses dados.
"""



def extrair_dados_do_endpoint(quantidade_informacao_geradas, **kwargs):
    ti = kwargs['ti']
    url = f"http://172.19.0.8:5000/dados-funcionarios_veiculo/{quantidade_informacao_geradas}"
    response = requests.get(url)

    print(response.raise_for_status() )

    data = response.json()
    print("Dados extraidos do endpoint:", data)

    ti.xcom_push(key='funcionario', value=data.get('tabela_funcionario'))
    ti.xcom_push(key='veiculo', value=data.get('tabela_veiculo'))


def funcionario(**kwargs):
    ti = kwargs['ti']
    funcionarios = ti.xcom_pull(task_ids='extrair_dados_do_endpoint', key='funcionario')

    # Preparar os dados para inserção em lote
    rows_to_insert = []
    for i in range(len(funcionarios['matricula'])):
        matricula = int(funcionarios['matricula'][i])
        nome_funcionario = funcionarios['nome_funcionario'][i]
        cargo = funcionarios['cargo'][i]
        nivel_hierarquico = funcionarios['nivel_hierarquico'][i]
        regiao = funcionarios['regiao'][i]
        email = funcionarios['email'][i]
        telefone = funcionarios['telefone'][i]

        row = (matricula, nome_funcionario, cargo, nivel_hierarquico, regiao, email, telefone)
        rows_to_insert.append(row)

    # Inserir em lote usando PostgresHook
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    
    # Executar a inserção em lote
    pg_hook.insert_rows(table='funcionario', rows=rows_to_insert, commit_every=1000)

def veiculo(**kwargs):
    ti = kwargs['ti']
    veiculo = ti.xcom_pull(task_ids='extrair_dados_do_endpoint', key='veiculo')

    rows_to_insert = []
    for i in range(len(veiculo['matricula'])):
        matricula = int(veiculo['matricula'][i])
        nome_funcionario = veiculo['nome_funcionario'][i]
        placa_veiculo = veiculo['placa_veiculo'][i]
        modelo_veiculo = veiculo['modelo_veiculo'][i]
        cor = veiculo['cor'][i]


        row = (matricula, nome_funcionario, placa_veiculo, modelo_veiculo, cor)
        rows_to_insert.append(row)

    # Inserir em lote usando PostgresHook
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    
    # Executar a inserção em lote
    pg_hook.insert_rows(table='veiculo', rows=rows_to_insert, commit_every=1000)
        

def postgres_to_csv_s3(**kwargs):
    # Conectar ao PostgreSQL usando o PostgresHook
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    
    # Definir a consulta SQL
    sql = 'SELECT * FROM estacionamento'
    
    # Executar a consulta e armazenar os resultados
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    
    # Obter os nomes das colunas
    colnames = [desc[0] for desc in cursor.description]
    
    # Criar um DataFrame a partir dos resultados
    df = pd.DataFrame(results, columns=colnames)
    df = df.drop_duplicates()
    

    hook = S3Hook(aws_conn_id='aws_default')
    caminho_s3 = ''
    current_date = datetime.now()
    year = current_date.year
    month = current_date.month
    
    with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.xlsx') as tmpfile:
        # Salvar o DataFrame em um arquivo Excel temporário
        df.to_excel(tmpfile.name, 'Sheet1', engine='openpyxl', index=False) 


        # Carregar o arquivo Excel para o S3
        hook.load_file(
            filename=tmpfile.name,
            key=f"{caminho_s3}estacionamento_elegibilidade_{year}-{month}.xlsx",
            bucket_name=bucket_name,
            replace=True
        )
        

with DAG(
    'estacionamento',
    default_args=default_args,
    description='Processo de EL e ETL',
    schedule_interval='@daily',
    start_date=days_ago(1),
    tags=['flask', 'postgresql']
) as dag:
    
    @task_group(group_id="criar_tabela", ui_color="blue")
    def criar_tabela():
        criar_tabela_sql_funcionario = """
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
"""

        criar_tabela_sql_veiculo = """
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
"""

        criar_tabela_funcionario_postgres_task = PostgresOperator(
            task_id='criar_tabela_funcionario_postgres',
            postgres_conn_id='postgres_conn',
            sql=criar_tabela_sql_funcionario
        )

        criar_tabela_veiculo_postgres_task = PostgresOperator(
            task_id='criar_tabela_veiculo_postgres',
            postgres_conn_id='postgres_conn',  
            sql=criar_tabela_sql_veiculo
        )

        criar_tabela_funcionario_postgres_task >> criar_tabela_veiculo_postgres_task


    extrair_dados_task = PythonOperator(
            task_id='extrair_dados_do_endpoint',
            python_callable=extrair_dados_do_endpoint,
            op_kwargs={'quantidade_informacao_geradas': 10000}
        )
    
    
    @task_group(group_id="inserir_dados_db", ui_color="blue")
    def inserir_para_db():

        inserir_funcionario_tabela_task = PythonOperator(
            task_id='inserir_funcionario_tabela_task',
            python_callable=funcionario,
            provide_context=True
        )
        
        inserir_veiculo_tabela_task = PythonOperator(
            task_id='inserir_veiculo_tabela_task',
            python_callable=veiculo,
            provide_context=True
        )

        inserir_funcionario_tabela_task >> inserir_veiculo_tabela_task


    transformacao_postgres_task = PostgresOperator(
        task_id='transformacao_postgres',
        postgres_conn_id='postgres_conn',  
        sql="""CREATE VIEW estacionamento AS
SELECT
    f.matricula AS Matrícula, 
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(f.nome_funcionario, 'Sr.', ''),
                        'Sra.', ''),
                    'Dr.', ''),
                'Srta.', ''),
            'Dra.', '') AS Nome_Funcionario, 
    f.cargo AS Cargo,
    f.nivel_hierarquico AS Nivel_Hierárquico, 
    v.placa_veiculo AS Placa_Veículo, 
    v.modelo_veiculo AS Modelo_Veículo, 
    v.cor AS Cor,
    CASE 
        WHEN f.nivel_hierarquico = 'Diretor' THEN 'Todos os estacionamentos'
        WHEN f.nivel_hierarquico = 'Equipe' THEN 'Lq303 e divina'
        WHEN f.nivel_hierarquico = 'Equipe Técnico Operacional' THEN 'Nenhum estacionamento'
        WHEN f.nivel_hierarquico = 'Gerente' THEN 'Divina e 695'
        WHEN f.nivel_hierarquico = 'Gerente Sr' THEN 'Divina, 70 e 695'
        WHEN f.nivel_hierarquico = 'Supervisor' THEN 'Lq303 e divina'
        WHEN f.nivel_hierarquico = 'Especialista' THEN 'Todos os estacionamentos'
    END AS Elegibilidade_Estacionamento,
    regiao AS Região,
        CASE 
            WHEN substr(REPLACE(REPLACE(f.telefone, '(', ''), ')', ''), 1, 1) = '0' 
                THEN CONCAT('+55 ', substr(REPLACE(REPLACE(REPLACE(telefone, '(', ''), ')', ''), '-', ' '), 2))
            WHEN length(f.telefone) = 12 
                THEN CONCAT('+55 ', REPLACE(REPLACE(REPLACE(f.telefone, '-', ' '), '(', ''), ')', ''))
            ELSE REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(f.telefone, '-', ' '), '(0', ''), ')', ' 9'), '(', ''), ')', '')
        END AS Telefone,
        REPLACE(
            REPLACE(
                REPLACE(f.email, '@example.org', '@hotmail.com'),
                '@example.com', '@gmail.com'),
            '@example.net', '@yahoo.com.br') AS Email
FROM funcionario f
JOIN veiculo v ON f.matricula = v.matricula;"""
    )
    bucket_name = 'estacionamento'
    caminho_s3 = ''

    postgres_to_csv_s3_task = PythonOperator(
        task_id='postgres_to_csv_s3_task',
        python_callable=postgres_to_csv_s3,
        provide_context=True,
        op_kwargs={'bucket_name': bucket_name, 'caminho_s3': caminho_s3}
    )

    criar_tabela() >> extrair_dados_task >> inserir_para_db() >> transformacao_postgres_task >> postgres_to_csv_s3_task
                                        
