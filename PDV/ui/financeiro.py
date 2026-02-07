import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def abrir_financeiro():
    conn = sqlite3.connect("db/pdv.db")
    cursor = conn.cursor()

    janela = tk.Toplevel()
    janela.title("Financeiro - Relatório de Vendas")

    # Tabela de vendas
    colunas = ("ID", "Data", "Forma Pagamento", "Valor Total")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(pady=10, fill="x")

    # Carregar vendas
    cursor.execute("SELECT id, data, forma_pagamento, valor_total FROM vendas ORDER BY data DESC")
    vendas = cursor.fetchall()
    for v in vendas:
        tree.insert("", "end", values=v)

    # Relatório por forma de pagamento
    cursor.execute("SELECT forma_pagamento, SUM(valor_total) FROM vendas GROUP BY forma_pagamento")
    resumo = cursor.fetchall()

    tk.Label(janela, text="Resumo por Forma de Pagamento", font=("Arial", 12, "bold")).pack(pady=10)
    for forma, total in resumo:
        tk.Label(janela, text=f"{forma}: R$ {total:.2f}", font=("Arial", 11)).pack(anchor="w")

    # Relatório diário
    cursor.execute("SELECT DATE(data), SUM(valor_total) FROM vendas GROUP BY DATE(data)")
    diario = cursor.fetchall()
    tk.Label(janela, text="Resumo Diário", font=("Arial", 12, "bold")).pack(pady=10)
    for dia, total in diario:
        tk.Label(janela, text=f"{dia}: R$ {total:.2f}", font=("Arial", 11)).pack(anchor="w")

    # Relatório mensal
    cursor.execute("SELECT strftime('%Y-%m', data), SUM(valor_total) FROM vendas GROUP BY strftime('%Y-%m', data)")
    mensal = cursor.fetchall()
    tk.Label(janela, text="Resumo Mensal", font=("Arial", 12, "bold")).pack(pady=10)
    for mes, total in mensal:
        tk.Label(janela, text=f"{mes}: R$ {total:.2f}", font=("Arial", 11)).pack(anchor="w")

    # Função para exportar CSV
    def exportar_csv():
        arquivo = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv")],
                                               title="Salvar relatório como")
        if arquivo:
            with open(arquivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Data", "Forma Pagamento", "Valor Total"])
                for v in vendas:
                    writer.writerow(v)
            messagebox.showinfo("Exportação concluída", f"Relatório salvo em:\n{arquivo}")

    tk.Button(janela, text="Exportar Relatório em CSV", command=exportar_csv).pack(pady=15)

    # Gráfico de barras e pizza
    formas = [f for f, _ in resumo]
    totais = [t for _, t in resumo]

    if formas and totais:
        fig, axs = plt.subplots(1, 2, figsize=(8, 4))

        # Gráfico de barras
        axs[0].bar(formas, totais, color="skyblue")
        axs[0].set_title("Vendas por Forma de Pagamento")
        axs[0].set_ylabel("Valor Total (R$)")

        # Gráfico de pizza
        axs[1].pie(totais, labels=formas, autopct="%1.1f%%", startangle=90)
        axs[1].set_title("Distribuição das Vendas")

        canvas = FigureCanvasTkAgg(fig, master=janela)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

    conn.close()
