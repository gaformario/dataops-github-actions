# Cálculos API

API Flask containerizada para operações matemáticas simples, com deploy automatizado via GitHub Actions em uma VM no Azure.

## Descrição

Esta API expõe endpoints para cálculos numéricos e demonstra conexão com banco de dados:

- `POST /operacao/soma`: recebe dois números e retorna a soma.
- `POST /operacao/multiplicacao`: recebe dois números e retorna o produto.
- `GET /alunos/`: retorna uma lista de alunos cadastrados no banco PostgreSQL (apenas para demonstração da conexão com o banco).

A documentação interativa da API está disponível em `http://48.211.168.205/swagger`.

## Tecnologias

- Python 3.10
- Flask + Flask-RESTX
- Docker & Docker Compose
- GitHub Actions (CI/CD)
- Azure VM
- (Opcional) PostgreSQL
