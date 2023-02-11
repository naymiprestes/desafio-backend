import os
from flask import Flask, render_template, request
import sqlite3
from unicodedata import normalize

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
def dados():

    arquivo = request.files.get('arquivo')
    arquivo.save(os.path.join('./', 'database.txt'))

    arquivo_aberto = open('database.txt')
    dados = []
    estabelecimentos = []
    transacoes = []
    saldos = []

    def valor(valor_transacao, tipo):
        if tipo in ['2', '3', '9']:
            return valor_transacao * (-1)
        else:
            return valor_transacao

    def palavras(palavra):
        string = normalize('NFD', palavra)
        string = string.encode('ASCII', 'ignore')
        string = string.decode('ASCII')
        return string
    
    for item in arquivo_aberto:
        dados.append((item[0:1], item[1:9], valor(float(item[9:19])/100.00, item[0:1]), item[19:30],
                      item[30:42], item[42:48], palavras(item[48:62].strip()), palavras(item[62:82].strip()),))
        

    banco = sqlite3.connect('db.sqlite')
    cursor = banco.cursor()
    cursor.execute('CREATE TABLE dados (tipo text, data text, valor real, cpf text, cartao text, hora text, dono text, loja text)')
    cursor.executemany("INSERT INTO dados(tipo, data, valor, cpf, cartao, hora, dono, loja) VALUES(?,?,?,?,?,?,?,?)", dados)
    banco.commit()
    cursor.execute('SELECT DISTINCT loja FROM dados')


    for item in cursor.fetchall():
        estabelecimentos.append(item[0])

    for item in estabelecimentos:
        data = cursor.execute('SELECT * FROM dados WHERE loja = ?', (item,))
        transacoes.append(data.fetchall())

    for item in estabelecimentos:
        cursor.execute('SELECT SUM(valor) FROM dados WHERE loja = ?', (item,))
        saldo = cursor.fetchall()[0][0]
        saldos.append(saldo)


         
    banco.close()
    arquivo_aberto.close()

    return render_template('upload.html', transacoes=transacoes, saldos=saldos)


if __name__ == '__main__':
    app.run(debug=True, port=8000)