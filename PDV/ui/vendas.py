import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def abrir_vendas():
    conn = sqlite3.connect("db/pdv.db")
    cursor = conn.cursor()

    janela = tk.Toplevel()
    janela.title("Registrar Venda")

    # Lista de produtos para seleção
    cursor.execute("SELECT id, nome, quantidade, estoque_minimo, estoque_maximo, valor_venda FROM produtos")
    produtos = cursor.fetchall()
    produto_dict = {f"{p[1]} (Estoque: {p[2]})": p for p in produtos}

    # Campos da venda
    tk.Label(janela, text="Produto:").grid(row=0, column=0)
    combo_produto = ttk.Combobox(janela, values=list(produto_dict.keys()))
    combo_produto.grid(row=0, column=1)

    tk.Label(janela, text="Quantidade:").grid(row=1, column=0)
    entry_quantidade = tk.Entry(janela)
    entry_quantidade.grid(row=1, column=1)

    # Tabela de itens da venda
    colunas = ("Produto", "Qtd", "Valor Unit", "Subtotal")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.grid(row=2, column=0, columnspan=2, pady=10)

    # Label para total
    label_total = tk.Label(janela, text="Total: R$ 0.00", font=("Arial", 12, "bold"))
    label_total.grid(row=3, column=0, columnspan=2)

    # Função para adicionar item
    def adicionar_item():
        produto_selecionado = combo_produto.get()
        if not produto_selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto.")
            return

        produto = produto_dict[produto_selecionado]
        produto_id, nome, estoque, estoque_min, estoque_max, valor_venda = produto

        try:
            qtd = float(entry_quantidade.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite uma quantidade válida.")
            return

        if qtd > estoque:
            messagebox.showerror("Erro", "Quantidade maior que o estoque disponível.")
            return

        subtotal = qtd * valor_venda
        tree.insert("", "end", values=(nome, qtd, f"R$ {valor_venda:.2f}", f"R$ {subtotal:.2f}"))

        atualizar_total()

    # Função para atualizar total
    def atualizar_total():
        total = 0
        for item in tree.get_children():
            valores = tree.item(item)["values"]
            subtotal = float(str(valores[3]).replace("R$", "").replace(",", "."))
            total += subtotal
        label_total.config(text=f"Total: R$ {total:.2f}")

    # Forma de pagamento
    tk.Label(janela, text="Forma de Pagamento:").grid(row=4, column=0)
    formas_pagamento = ["Pix", "Dinheiro", "Cartão Débito", "Cartão Crédito", "Promissória"]
    combo_pagamento = ttk.Combobox(janela, values=formas_pagamento)
    combo_pagamento.grid(row=4, column=1)

    # Função para registrar venda
    def registrar_venda():
        if not tree.get_children():
            messagebox.showwarning("Atenção", "Nenhum item na venda.")
            return

        forma_pagamento = combo_pagamento.get()
        if not forma_pagamento:
            messagebox.showwarning("Atenção", "Selecione a forma de pagamento.")
            return

        # Calcula total
        total = float(label_total.cget("text").replace("Total: R$", "").strip())

        # Salva venda
        cursor.execute("INSERT INTO vendas (forma_pagamento, valor_total) VALUES (?, ?)",
                       (forma_pagamento, total))
        venda_id = cursor.lastrowid

        # Salva itens da venda
        for item in tree.get_children():
            valores = tree.item(item)["values"]
            nome_produto, qtd, valor_unit, subtotal = valores
            qtd = float(qtd)
            valor_unit = float(str(valor_unit).replace("R$", "").replace(",", "."))
            subtotal = float(str(subtotal).replace("R$", "").replace(",", "."))

            cursor.execute("SELECT id, quantidade FROM produtos WHERE nome=?", (nome_produto,))
            produto = cursor.fetchone()
            if produto:
                produto_id, estoque_atual = produto
                novo_estoque = estoque_atual - qtd
                cursor.execute("UPDATE produtos SET quantidade=? WHERE id=?", (novo_estoque, produto_id))

                cursor.execute("""INSERT INTO itens_venda 
                                  (venda_id, produto_id, quantidade, valor_unitario, subtotal)
                                  VALUES (?, ?, ?, ?, ?)""",
                               (venda_id, produto_id, qtd, valor_unit, subtotal))

        conn.commit()

        messagebox.showinfo("Venda registrada", f"Venda concluída!\nForma de pagamento: {forma_pagamento}\nValor total: R$ {total:.2f}")
        janela.destroy()

    # Botões
    tk.Button(janela, text="Adicionar Item", command=adicionar_item).grid(row=5, column=0, pady=10)
    tk.Button(janela, text="Registrar Venda", command=registrar_venda).grid(row=5, column=1, pady=10)
