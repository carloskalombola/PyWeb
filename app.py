from flask import Flask, render_template, g, request, redirect, session, url_for, flash, abort
import sqlite3


app = Flask("Olá")
DATABASE = "banco.bd"
SECRET_KEY = "1234"

app.config.from_object(__name__)



def conectar():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.bd =  conectar()

@app.teardown_request
def teardown_request(f):
    g.bd.close()

@app.route("/")
def display_posts():
    sql = "SELECT titulo, texto, data_criacao FROM posts ORDER BY id DESC"
    resultado = g.bd.execute(sql)
    post = []

    for titulo, texto, data_criacao in resultado.fetchall():
        post.append({
            "titulo":titulo,
            "texto":texto,
            "data_criacao":data_criacao
           })
    return render_template("display_posts.html", post=post)

@app.route("/inserir", methods= ["POST", "GET"])
def inserir():
    if not session.get('logado'):
        abort(401)
    titulo = request.form.get('titulo')
    texto = request.form.get('texto')
    sql = "INSERT INTO posts (titulo, texto) VALUES (?, ?)"
    g.bd.execute(sql,[titulo, texto])
    g.bd.commit()
    flash("Novo post inserido")
    return redirect(url_for('display_posts'))




@app.route("/login",  methods= ["POST", "GET"])
def login():
    erro = None
    if (request.method == "POST"):
        if request.form['username'] == "Web" and request.form['password'] == "web1234":
            session['logado']  = True
            flash("Usuário logado com sucesso!" + request.form['username'])
            return redirect(url_for('display_posts'))
        erro="Usuáio ou senha incorretos"
    return render_template("login.html", erro=erro)

@app.route("/logout")
def logout():
    session.pop('logado', None)

    flash("Logout efetuado com sucesso")
    return redirect(url_for('display_posts'))