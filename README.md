# estacionamento-etl

# Arquitetura final do projeto

CASE DO PROJETO: 
  - Neste projeto, O gestor da área de dados da minha empresa Lobobranco LTDA, propos a criação de uma pipeline de dados para gerenciar e processar dados consumidos de uma API própria da empresa. A pipeline tem como objetivo      - criar tabelas com relacionamento, transformar os dados e gerar uma view temporária normalizada.

  - Esse processo consiste em várias etapas:
    - EL e ETL 
    - Consumo de Dados da API: Os dados são consumidos de uma API própria da empresa.
    - Transformação dos Dados: Os dados consumidos são transformados e organizados em tabelas relacionadas.
    - Criação de View Temporária Normalizada: Uma view temporária normalizada é criada a partir dos dados transformados.
    - Exportação para S3: A view temporária normalizada é exportada para um bucket S3 em formato Excel (.xlsx).
    - Sistema de Consulta: Com base no arquivo Excel exportado, é criado um sistema de consulta por matrícula.
  Este procedimento é realizado uma vez por mês, garantindo que os dados estejam sempre atualizados e acessíveis para consulta conforme necessário.
  Esta abordagem permite uma gestão eficiente dos dados, garantindo sua integridade e disponibilidade para análise e consulta, atendendo às necessidades do gestor e da empresa.

# Projeto de EL (Extract and Load) com Docker, Flask, Airflow e PostgreSQL
  - Este projeto automatiza o processo de Extração e Carga (EL) de dados fictícios de funcionários e veículos brasileiros utilizando Flask para geração de dados aleatórios e Airflow para orquestração do fluxo de trabalho. Os dados extraídos são armazenados em tabelas PostgreSQL.

### Funcionalidades

- Flask API:
  Gera dados fictícios de funcionários e veículos através de um endpoint REST.
  Executa dentro de um container Docker.

- Airflow DAG:
  Orquestra o processo de EL.
  Cria tabelas no PostgreSQL.
  Extrai dados da API Flask.
  Insere os dados extraídos nas tabelas correspondentes do PostgreSQL.

- Diagrama de classes 
<div align="center">
<img src="https://github.com/lobobranco96/airflow-flask-rds/assets/131804750/1d85081e-9e19-4044-9e4e-fac94c177f7c" width="900px" />
</div>

- Planilha de cadastr
  
<div align="center">
<img src="(https://github.com/lobobranco96/estacionamento-etl/assets/131804750/96199c26-e903-40db-9561-6935922b9ea8)" width="00px" />
</div>

### Pré-requisitos
Docker instalado localmente para execução da aplicação Flask.
Airflow configurado localmente ou em um ambiente de execução, com conexões configuradas para o PostgreSQL.


### Estrutura do Projeto

``` ├── README.md
└── airflow-docker/
    ├── docker-compose.yaml
    ├── Dockerfile
    ├── requirements.txt
    ├── dags/
    │   └── application.py  # DAG principal do Airflow
    |   ├── flask_app/
    |   │   ├── app.py  # Aplicação Flask para geração de dados
    |   │   ├── requirements_flask.txt  # Requisitos específicos da aplicação Flask
    |   │   └── Dockerfile  # Dockerfile para a aplicação Flask
    └── plugins/
    └── images/  # Diretório para imagens dos processos concluidos.```


/dags/flask_app/: Contém a aplicação Flask para geração de dados fictícios.

  - Dockerfile: Configurações para construção da imagem Docker da aplicação Flask e para executar o Airflow.
  - docker-compose.yaml: Arquivo de configuração do Docker Compose para executar o airflow e a aplicação Flask.
  - airflow/: Configurações do Airflow para execução do DAG.
  - dags/: Diretório onde os arquivos DAG do Airflow são armazenados.
  - plugins/: Diretório opcional para plugins do Airflow.

Configuração e Uso
Clonar o repositório:

bash
git clone https://github.com/lobobranco96/estacionamento-etl.git
cd airflow-docker

## Configurar e iniciar o Flask:

No diretório airflow-flask-rds/, execute:
bash
docker build -t flask_airflow 
docker-compose up

Isso iniciará o processo de build de um container Docker.

É necessario configurar as connections necessarias na UI do airflow para funcionamento da aplicação. Voce vai encontrar o exemplo no diretorio images.
Se precisar utilizar um banco de dados local, segue a configuração.
No connections do airflow preencha nesse formato.
  - Conn id: postgres_conn
  - Host: host.docker.internal
  - login : airflow
  - password: airflow
  - port : 5432

### Executar o DAG do Airflow:

Acesse o painel do Airflow em http://localhost:8080 (ou outro endereço conforme configurado) para monitorar e executar o DAG application.py


Personalização e Contribuição:

Sinta-se à vontade para personalizar o projeto conforme suas necessidades.
Contribuições são bem-vindas! Abra uma issue para discutir grandes alterações antes de enviar um pull request.
Licença
