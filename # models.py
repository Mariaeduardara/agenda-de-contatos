# models.py
class Contato:
    def __init__(self, nome: str, telefone: str, email: str):
        self.nome = nome
        self.telefone = telefone
        self.email = email

    def __str__(self):
        return f"{self.nome} - {self.telefone} - {self.email}"
