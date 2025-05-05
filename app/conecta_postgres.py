from flask import Flask, request
from flask_restx import Api, Resource, fields
import os
import psycopg2
import time

app = Flask(__name__)
api = Api(app, version='1.0', title='Alunos API',
          description='API para cadastro e consulta de alunos',
          doc='/swagger')

ns = api.namespace('alunos', description='Operações relacionadas a alunos')

soma_model = api.model('Soma', {
    'a': fields.Float(required=True, description='Primeiro número'),
    'b': fields.Float(required=True, description='Segundo número')
})

multiplicacao_model = api.model('Multiplicacao', {
    'a': fields.Float(required=True, description='Primeiro número'),
    'b': fields.Float(required=True, description='Segundo número')
})

def get_connection():
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host=os.environ.get("DB_HOST", "db"),
                database=os.environ.get("DB_NAME", "postgres"),
                user=os.environ.get("DB_USER", "postgres"),
                password=os.environ.get("DB_PASS", "senha123")
            )
            return conn
        except psycopg2.OperationalError:
            print("Banco não está pronto, tentando novamente...")
            time.sleep(3)
    raise Exception("Não foi possível conectar ao banco de dados.")

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

@api.route('/soma')
class Soma(Resource):
    @api.expect(soma_model)
    def post(self):
        """Recebe dois números e retorna a soma"""
        data = request.get_json()
        a = data.get('a')
        b = data.get('b')
        if a is None or b is None:
            return {'error': 'Parâmetros a e b são obrigatórios'}, 400
        return {'resultado': a + b}

@api.route('/multiplicacao')
class Multiplicacao(Resource):
    @api.expect(multiplicacao_model)
    def post(self):
        """Recebe dois números e retorna o produto"""
        data = request.get_json()
        a = data.get('a')
        b = data.get('b')
        if a is None or b is None:
            return {'error': 'Parâmetros a e b são obrigatórios'}, 400
        return {'resultado': a * b}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)