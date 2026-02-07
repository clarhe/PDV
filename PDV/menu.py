import tkinter as tk
from ui.cadastro_produto import abrir_cadastro_produto   # importa a tela de cadastro de produtos
from ui.estoque import abrir_estoque                     # importa a tela de controle de estoque
from ui.vendas import abrir_vendas                       # importa a tela de vendas
from ui.financeiro import abrir_financeiro               # importa a tela de financeiro

def abrir_menu(usuario_nome="Usuário"):
    # Cria nova janela para o menu principal
    menu = tk.Toplevel()  # Usamos Toplevel para abrir uma nova janela a partir do main.py
    menu.title("Mapa do Sistema - PDV")

    # Mensagem de boas-vindas
    tk.Label(menu, text=f"Bem-vindo, {usuario_nome}!", font=("Arial", 14)).pack(pady=10)

    # Botões de navegação
    tk.Button(menu, text="Cadastro de Produtos", width=25,
              command=abrir_cadastro_produto).pack(pady=5)

    tk.Button(menu, text="Controle de Estoque", width=25,
              command=abrir_estoque).pack(pady=5)

    tk.Button(menu, text="Vendas", width=25,
              command=abrir_vendas).pack(pady=5)

    tk.Button(menu, text="Financeiro", width=25,
              command=abrir_financeiro).pack(pady=5)

    tk.Button(menu, text="Sair", width=25, command=menu.destroy).pack(pady=10)

# Teste rápido: se rodar direto menu.py
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # esconde a janela principal
    abrir_menu("Vanessa")
    root.mainloop()
