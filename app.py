from flask import Flask

app = Flask("Olá")

@app.route('/')
def ola():
    return "Olá mundo, bom dia"

@app.route('/alunos')
def alunos():
    return
