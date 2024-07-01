FROM python:3.9-slim

WORKDIR /opt/airflow/dags/flask_app

COPY ./requirements_flask.txt /requirements_flask.txt
RUN pip install --no-cache-dir -r /requirements_flask.txt

COPY . .

CMD ["python", "app.py"]
