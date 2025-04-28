import psycopg2
import time
from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version='1.0', title='Alunos API',
          description='API para cadastro e consulta de alunos',
          doc='/swagger')

ns = api.namespace('alunos', description='Operações relacionadas a alunos')

def get_connection():
    conn = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="senha123"
    )
    return conn

@ns.route('/')
class AlunosList(Resource):
    def get(self):
        """Lista todos os alunos"""
        time.sleep(5)  # Espera o banco iniciar
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(50)
            );
        """)
        conn.commit()
        cur.execute("INSERT INTO alunos (nome) VALUES ('Maria'), ('João') ON CONFLICT DO NOTHING;")
        conn.commit()
        cur.execute("SELECT * FROM alunos;")
        alunos = cur.fetchall()
        cur.close()
        conn.close()
        return {"alunos": [{"id": aluno[0], "nome": aluno[1]} for aluno in alunos]}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)