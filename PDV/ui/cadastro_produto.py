import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

def abrir_cadastro_produto():
    conn = sqlite3.connect("db/pdv.db")
    cursor = conn.cursor()

    janela = tk.Toplevel()
    janela.title("Cadastro de Produtos")

    # Campos
    tk.Label(janela, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(janela)
    entry_nome.grid(row=0, column=1)

    tk.Label(janela, text="Descrição:").grid(row=1, column=0)
    entry_descricao = tk.Entry(janela)
    entry_descricao.grid(row=1, column=1)

    tk.Label(janela, text="Quantidade:").grid(row=2, column=0)
    entry_quantidade = tk.Entry(janela)
    entry_quantidade.grid(row=2, column=1)

    tk.Label(janela, text="Tipo de Quantidade:").grid(row=3, column=0)
    tipo_quantidade = ttk.Combobox(janela, values=["Peso", "Unidade", "Caixa"])
    tipo_quantidade.grid(row=3, column=1)

    tk.Label(janela, text="Valor de Compra:").grid(row=4, column=0)
    entry_valor_compra = tk.Entry(janela)
    entry_valor_compra.grid(row=4, column=1)

    tk.Label(janela, text="Estoque Mínimo:").grid(row=5, column=0)
    entry_estoque_minimo = tk.Entry(janela)
    entry_estoque_minimo.grid(row=5, column=1)

    tk.Label(janela, text="Estoque Máximo:").grid(row=6, column=0)
    entry_estoque_maximo = tk.Entry(janela)
    entry_estoque_maximo.grid(row=6, column=1)

    tk.Label(janela, text="Valor de Venda:").grid(row=7, column=0)
    entry_valor_venda = tk.Entry(janela)
    entry_valor_venda.grid(row=7, column=1)

    # Função para salvar
    def salvar():
        try:
            cursor.execute("""
                INSERT INTO produtos (nome, descricao, quantidade, tipo_quantidade, valor_compra, estoque_minimo, estoque_maximo, valor_venda)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry_nome.get(),
                entry_descricao.get(),
                float(entry_quantidade.get()),
                tipo_quantidade.get(),
                float(entry_valor_compra.get()),
                int(entry_estoque_minimo.get()),
                int(entry_estoque_maximo.get()),
                float(entry_valor_venda.get())
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

    tk.Button(janela, text="Salvar", command=salvar).grid(row=8, column=0, columnspan=2, pady=10)
