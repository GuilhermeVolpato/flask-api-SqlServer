import os
import pyodbc
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()
# Conexão com o banco de dados


app = Flask(__name__)

server = os.getenv('server')
database = os.getenv('database')
username = os.getenv('usernameBanco')
password = os.getenv('password')

# Criação da string de conexão
connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(connection_string)

@app.get('/')
def home():
  return '200'

@app.post('/funcionarios/insert')
def post_funcionarios():
    data = request.json
    id_funcionario = data['id_funcionario']
    nome = data['nome']
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO funcionarios (id_funcionario, nome) VALUES (?, ?)", (id_funcionario, nome))
    conn.commit()
    return {'message': 'Funcionário cadastrado com sucesso!'}


@app.get('/funcionarios')
def get_funcionarios():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM funcionarios')
    rows = cursor.fetchall()

    funcionarios = []
    for row in rows:
        funcionario = {
            'id_funcionario': row.id_funcionario,
            'nome': row.nome
        }
        funcionarios.append(funcionario)

    return {'funcionarios': funcionarios}