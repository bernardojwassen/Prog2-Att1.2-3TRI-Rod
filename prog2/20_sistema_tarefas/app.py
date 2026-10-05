"""Exercício 20 — Sistema de tarefas (Flask + SQLite). Rodar: pip install flask && python app.py"""
import sqlite3
from flask import Flask, jsonify, request, render_template

DB = "tarefas.db"
app = Flask(__name__)


class Tarefa:
    """Entidade do sistema (orientação a objetos, com validação no setter)."""
    def __init__(self, id, titulo, concluida=False):
        self.id = id
        self.titulo = titulo
        self.concluida = bool(concluida)

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        valor = (valor or "").strip()
        if not valor or len(valor) > 100:
            raise ValueError("O título é obrigatório (máx. 100 caracteres).")
        self._titulo = valor

    def to_dict(self):
        return {"id": self.id, "titulo": self.titulo, "concluida": self.concluida}


def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def iniciar_banco():
    with conectar() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            concluida INTEGER NOT NULL DEFAULT 0)""")


def listar():
    """Estrutura de dados: LISTA de objetos Tarefa, na ordem de cadastro."""
    with conectar() as con:
        return [Tarefa(r["id"], r["titulo"], r["concluida"])
                for r in con.execute("SELECT * FROM tarefas ORDER BY id")]


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/tarefas")                      # READ
def api_listar():
    return jsonify([t.to_dict() for t in listar()])


@app.post("/api/tarefas")                     # CREATE
def api_criar():
    try:
        t = Tarefa(None, (request.get_json() or {}).get("titulo"))
    except ValueError as e:
        return jsonify(erro=str(e)), 400
    with conectar() as con:
        t.id = con.execute("INSERT INTO tarefas (titulo) VALUES (?)", (t.titulo,)).lastrowid
    return jsonify(t.to_dict()), 201


@app.put("/api/tarefas/<int:id>")             # UPDATE
def api_alterar(id):
    dados = request.get_json() or {}
    with conectar() as con:
        r = con.execute("SELECT * FROM tarefas WHERE id = ?", (id,)).fetchone()
        if not r:
            return jsonify(erro="Tarefa não encontrada."), 404
        t = Tarefa(r["id"], r["titulo"], r["concluida"])
        try:
            if "titulo" in dados:
                t.titulo = dados["titulo"]
        except ValueError as e:
            return jsonify(erro=str(e)), 400
        if "concluida" in dados:
            t.concluida = bool(dados["concluida"])
        con.execute("UPDATE tarefas SET titulo = ?, concluida = ? WHERE id = ?",
                    (t.titulo, int(t.concluida), id))
    return jsonify(t.to_dict())


@app.delete("/api/tarefas/<int:id>")          # DELETE
def api_excluir(id):
    with conectar() as con:
        if con.execute("DELETE FROM tarefas WHERE id = ?", (id,)).rowcount == 0:
            return jsonify(erro="Tarefa não encontrada."), 404
    return "", 204


if __name__ == "__main__":
    iniciar_banco()
    app.run(debug=True)
