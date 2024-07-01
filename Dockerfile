FROM apache/airflow:2.7.1-python3.11

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


USER airflow

COPY ./requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

COPY --chown=airflow:root ./dags /opt/airflow/dags