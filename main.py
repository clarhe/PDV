import sys
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
from menu import abrir_menu   # importa o menu principal

# Função para localizar recursos (funciona no .py e no .exe)
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Caminho do banco de dados dentro da pasta db
db_path = resource_path(os.path.join("db", "pdv.db"))

# Conexão com banco de dados
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Função para cadastrar novo usuário
def cadastrar_usuario():
    nome = entry_nome.get()
    sobrenome = entry_sobrenome.get()
    login = entry_login.get()
    senha = entry_senha.get()

    if not nome or not sobrenome or not login or not senha:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, sobrenome, login, senha) VALUES (?, ?, ?, ?)",
            (nome, sobrenome, login, senha)
        )
        conn.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
        abrir_menu(nome)  # Abre o menu após cadastro
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Login já existe. Use outro login.")

# Função para login
def login_usuario():
    login = entry_login.get()
    senha = entry_senha.get()

    cursor.execute("SELECT * FROM usuarios WHERE login=? AND senha=?", (login, senha))
    usuario = cursor.fetchone()

    if usuario:
        messagebox.showinfo("Bem-vindo", f"Olá {usuario[1]} {usuario[2]}! Você entrou no sistema.")
        abrir_menu(usuario[1])  # Abre o menu passando o nome
    else:
        messagebox.showerror("Erro", "Login ou senha inválidos.")

# Interface gráfica
root = tk.Tk()
root.title("Cadastro/Login de Usuário - PDV")
root.geometry("1024x768")  # largura x altura da janela

tk.Label(root, text="Nome:").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Sobrenome:").grid(row=1, column=0)
entry_sobrenome = tk.Entry(root)
entry_sobrenome.grid(row=1, column=1)

tk.Label(root, text="Login:").grid(row=2, column=0)
entry_login = tk.Entry(root)
entry_login.grid(row=2, column=1)

tk.Label(root, text="Senha:").grid(row=3, column=0)
entry_senha = tk.Entry(root, show="*")
entry_senha.grid(row=3, column=1)

tk.Button(root, text="Cadastrar", command=cadastrar_usuario).grid(row=4, column=0, pady=5)
tk.Button(root, text="Entrar", command=login_usuario).grid(row=4, column=1, pady=5)

root.mainloop()
