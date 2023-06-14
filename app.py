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
# Tomar cuidado com o DRIVER utilizado, pois pode variar de acordo com a versão do SQL Server instalada!
connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
conn = pyodbc.connect(connection_string)

@app.get('/')
def home():
  return '200'

@app.post('/cardapio/insert')
def create_cardapio():
    data = request.json
    id_cardapio = data['id_cardapio']
    nome = data['nome']
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO cardapio (id_cardapio, nome) VALUES (?, ?)", (id_cardapio, nome))
    conn.commit()
    return {'message': 'Funcionário cadastrado com sucesso!'}


@app.get('/cardapio/read')
def read_cardapio():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cardapio')
    rows = cursor.fetchall()

    funcionarios = []
    for row in rows:
        funcionario = {
            'id_cardapio': row.id_cardapio,
            'nome': row.nome
        }
        funcionarios.append(funcionario)

    return {'cardapio': funcionarios}

@app.post('/cardapio/update')
def update_cardapio():
    data = request.json
    id_cardapio = data['id_cardapio']
    nome = data['nome']
    cursor = conn.cursor()
    cursor.execute(f"UPDATE cardapio SET nome = ? WHERE id_cardapio = ?", (nome, id_cardapio))
    conn.commit()
    return {'message': 'cardapio atualizado com sucesso!'}

@app.post('/cardapio/delete')
def delete_cardapio():
    data = request.json
    id_cardapio = data['id_cardapio']
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM cardapio WHERE id_cardapio = ?", (id_cardapio))
    conn.commit()
    return {'message': 'cardapio deletado com sucesso!'}