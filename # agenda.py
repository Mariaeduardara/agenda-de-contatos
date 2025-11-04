# agenda.py
import sqlite3
from models import Contato

class Agenda:
    def __init__(self, db_name="contatos.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT,
                email TEXT
            )
        """)
        self.conn.commit()

    def adicionar(self, contato: Contato):
        self.cursor.execute(
            "INSERT INTO contatos (nome, telefone, email) VALUES (?, ?, ?)",
            (contato.nome, contato.telefone, contato.email)
        )
        self.conn.commit()

    def listar(self):
        self.cursor.execute("SELECT nome, telefone, email FROM contatos")
        return [Contato(nome, telefone, email) for nome, telefone, email in self.cursor.fetchall()]

    def remover(self, nome: str):
        self.cursor.execute("DELETE FROM contatos WHERE nome = ?", (nome,))
        self.conn.commit()

    def fechar(self):
        self.conn.close()
