FROM python:3.10-slim

WORKDIR /app

COPY api-flask.py .

RUN pip install psycopg2-binary flask flask-restx gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api-flask:app"]