from flask import Flask, request
from flask_restx import Api, Resource, fields
import os
import psycopg2
import time

app = Flask(__name__)
api = Api(app, version='1.0', title='Cálculos API',
          description='API para cálculos numéricos',
          doc='/swagger')

ns = api.namespace('Cálculos', description='Cálculos numéricos')

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
@ns.route('/soma')
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

@ns.route('/multiplicacao')
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