# app_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from models import Contato
from agenda import Agenda

class AgendaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Agenda de Contatos")
        self.root.geometry("500x430")
        self.root.configure(bg="#f0f2f5")
        self.root.resizable(False, False)

        # instância única do Agenda (mesmo DB)
        self.agenda = Agenda()

        # Título
        title = tk.Label(root, text="📖 Agenda de Contatos", font=("Helvetica", 16, "bold"), bg="#f0f2f5", fg="#333")
        title.pack(pady=10)

        # Formulário
        frame_form = tk.Frame(root, bg="#f0f2f5")
        frame_form.pack(pady=5)

        tk.Label(frame_form, text="Nome:", bg="#f0f2f5").grid(row=0, column=0, sticky="e")
        tk.Label(frame_form, text="Telefone:", bg="#f0f2f5").grid(row=1, column=0, sticky="e")
        tk.Label(frame_form, text="E-mail:", bg="#f0f2f5").grid(row=2, column=0, sticky="e")

        self.entry_nome = tk.Entry(frame_form, width=35)
        self.entry_telefone = tk.Entry(frame_form, width=35)
        self.entry_email = tk.Entry(frame_form, width=35)

        self.entry_nome.grid(row=0, column=1, pady=2)
        self.entry_telefone.grid(row=1, column=1, pady=2)
        self.entry_email.grid(row=2, column=1, pady=2)

        # Botões
        frame_btn = tk.Frame(root, bg="#f0f2f5")
        frame_btn.pack(pady=10)

        ttk.Button(frame_btn, text="Adicionar", command=self.adicionar_contato).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btn, text="Remover", command=self.remover_contato).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btn, text="Atualizar lista", command=self.atualizar_lista).grid(row=0, column=2, padx=5)

        # Treeview (lista)
        self.tree = ttk.Treeview(root, columns=("nome", "telefone", "email"), show="headings", height=12)
        self.tree.heading("nome", text="Nome")
        self.tree.heading("telefone", text="Telefone")
        self.tree.heading("email", text="E-mail")
        self.tree.column("nome", width=170)
        self.tree.column("telefone", width=120)
        self.tree.column("email", width=200)
        self.tree.pack(pady=10)

        # Carrega a lista inicial
        self.atualizar_lista()

    def adicionar_contato(self):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()

        if not nome:
            messagebox.showwarning("Aviso", "O nome não pode estar vazio.")
            return

        try:
            contato = Contato(nome, telefone, email)
            self.agenda.adicionar(contato)
            print(f"[DEBUG] Adicionado no DB: {nome}, {telefone}, {email}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao adicionar contato: {e}")
            print(f"[ERROR] adicionar_contato: {e}")
            return

        self.limpar_campos()
        # força atualizar imediatamente
        self.atualizar_lista()

    def remover_contato(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um contato para remover.")
            return

        valores = self.tree.item(selecionado, "values")
        nome = valores[0]
        try:
            self.agenda.remover(nome)
            print(f"[DEBUG] Removido do DB: {nome}")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao remover contato: {e}")
            print(f"[ERROR] remover_contato: {e}")
            return

        # força atualizar imediatamente
        self.atualizar_lista()

    def atualizar_lista(self):
        # Limpa o Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tenta carregar do banco
        try:
            contatos = self.agenda.listar()
            print(f"[DEBUG] contatos carregados: {len(contatos)}")  # debug no terminal
            if not contatos:
                # mostra linha vazia informativa
                self.tree.insert("", "end", values=("Nenhum contato cadastrado", "", ""))
            else:
                for c in contatos:
                    # garante valores strings
                    nome = c.nome if c.nome is not None else ""
                    tel = c.telefone if c.telefone is not None else ""
                    email = c.email if c.email is not None else ""
                    self.tree.insert("", "end", values=(nome, tel, email))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar a lista: {e}")
            print(f"[ERROR] atualizar_lista: {e}")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    def on_close(self):
        try:
            self.agenda.fechar()
        except Exception:
            pass
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AgendaApp(root)
    # liga fechamento para fechar conexão DB
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
