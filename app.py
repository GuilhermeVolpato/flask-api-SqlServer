import os
import pyodbc
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

load_dotenv()
# Conexão com o banco de dados

app = Flask(__name__)
CORS(app)

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
    id_item_cardapio = data['id_item_cardapio']
    nome_item = data['nome_item']
    valor = data['valor']
    descricao = data['descricao']
    categoria = data['categoria']
    disponibilidade = data['disponibilidade']
    id_estoque = data['id_estoque']
    quantidade = data['quantidade']
    unidade = data.get('unidade')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM estoque WHERE id_estoque = ?", (id_estoque,))
    result = cursor.fetchone()

    if result[0] > 0:  # Verifica se o valor de id_estoque existe na tabela estoque
        cursor.execute("INSERT INTO cardapio (id_item_cardapio, nome_item, valor, descricao, categoria, disponibilidade) VALUES (?, ?, ?, ?, ?, ?)",
                       (id_item_cardapio, nome_item, valor, descricao, categoria, disponibilidade))
        if unidade is not None:
            cursor.execute("INSERT INTO ingredientes (id_item_cardapio, id_estoque, quantidade, unidade) VALUES (?, ?, ?, ?)",
                           (id_item_cardapio, id_estoque, quantidade, unidade))
        else:
            cursor.execute("INSERT INTO ingredientes (id_item_cardapio, id_estoque, quantidade) VALUES (?, ?, ?)",
                           (id_item_cardapio, id_estoque, quantidade))
        conn.commit()
        return {'message': 'Item cadastrado com sucesso!'}
    else:
        return {'error': 'Não foi possível cadastrar o item, pois o id_estoque informado não existe na tabela estoque.'}


@app.get('/cardapio/read')
def read_cardapio():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cardapio')
    rows = cursor.fetchall()

    cardapios = []  # formata a resposta da requisição
    for row in rows:
        cardapio = {
            'id_item_cardapio': row.id_item_cardapio,
            'nome_item': row.nome_item,
            'valor': row.valor,
            'descricao': row.descricao,
            'categoria': row.categoria,
            'disponibilidade': row.disponibilidade
        }
        cardapios.append(cardapio)

    return {'cardapio': cardapios}

@app.post('/cardapio/update')
def update_cardapio():
    data = request.json
    id_item_cardapio = data['id_item_cardapio']
    nome_item = data.get('nome_item')
    valor = data.get('valor')
    descricao = data.get('descricao')
    categoria = data.get('categoria')
    disponibilidade = data.get('disponibilidade')
    
    cursor = conn.cursor()
    update_values = []
    query = "UPDATE cardapio SET "

    if nome_item:
        query += "nome_item = ?, "
        update_values.append(nome_item)
    
    if valor:
        query += "valor = ?, "
        update_values.append(valor)

    if descricao:
        query += "descricao = ?, "
        update_values.append(descricao)

    if categoria:
        query += "categoria = ?, "
        update_values.append(categoria)

    if disponibilidade is not None:
        query += "disponibilidade = ?, "
        update_values.append(disponibilidade)

    # Remove a última vírgula e espaço da query
    query = query[:-2]
    
    query += " WHERE id_item_cardapio = ?"
    update_values.append(id_item_cardapio)

    cursor.execute(query, update_values)
    conn.commit()
    
    return {'message': 'Cardápio atualizado com sucesso!'}


@app.post('/cardapio/delete')
def delete_cardapio():
    data = request.json
    id_item_cardapio = data['id_item_cardapio']
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM ingredientes WHERE id_item_cardapio = ?", (id_item_cardapio,))
    cursor.execute(f"DELETE FROM cardapio WHERE id_item_cardapio = ?", (id_item_cardapio))
    conn.commit()
    return {'message': 'cardapio deletado com sucesso!'}