import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def abrir_estoque():
    conn = sqlite3.connect("db/pdv.db")
    cursor = conn.cursor()

    janela = tk.Toplevel()
    janela.title("Controle de Estoque")

    # Tabela de produtos
    colunas = ("ID", "Nome", "Descrição", "Quantidade", "Tipo", "Valor Compra", "Estoque Min", "Estoque Max", "Valor Venda")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(fill="both", expand=True)

    # Função para carregar produtos
    def carregar_produtos():
        for item in tree.get_children():
            tree.delete(item)
        cursor.execute("SELECT * FROM produtos")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    carregar_produtos()

    # Função para excluir produto
    def excluir_produto():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto para excluir.")
            return
        item = tree.item(selecionado)
        produto_id = item["values"][0]
        cursor.execute("DELETE FROM produtos WHERE id=?", (produto_id,))
        conn.commit()
        carregar_produtos()
        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

    # Função para editar produto
    def editar_produto():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto para editar.")
            return
        item = tree.item(selecionado)
        produto = item["values"]

        edit_win = tk.Toplevel(janela)
        edit_win.title("Editar Produto")

        labels = ["Nome", "Descrição", "Quantidade", "Tipo", "Valor Compra", "Estoque Min", "Estoque Max", "Valor Venda"]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(edit_win, text=label).grid(row=i, column=0)
            entry = tk.Entry(edit_win)
            entry.insert(0, produto[i+1])  # pula o ID
            entry.grid(row=i, column=1)
            entries.append(entry)

        def salvar_edicao():
            cursor.execute("""
                UPDATE produtos SET nome=?, descricao=?, quantidade=?, tipo_quantidade=?, valor_compra=?, estoque_minimo=?, estoque_maximo=?, valor_venda=?
                WHERE id=?
            """, (
                entries[0].get(),
                entries[1].get(),
                float(entries[2].get()),
                entries[3].get(),
                float(entries[4].get()),
                int(entries[5].get()),
                int(entries[6].get()),
                float(entries[7].get()),
                produto[0]
            ))
            conn.commit()
            carregar_produtos()
            edit_win.destroy()
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

        tk.Button(edit_win, text="Salvar", command=salvar_edicao).grid(row=len(labels), column=0, columnspan=2, pady=10)

    # Botões de ação
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Atualizar", command=carregar_produtos).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Editar", command=editar_produto).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Excluir", command=excluir_produto).grid(row=0, column=2, padx=5)
