from flask import Flask

app = Flask("Olá")

@app.route('/')

def Ola():
    return "Olá mundo"
