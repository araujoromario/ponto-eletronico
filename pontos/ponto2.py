import tkinter as tk
from datetime import datetime
import os


def registrar_ponto():
    # Obter a data e hora atual
    data_hora_atual = datetime.now()

    # Formatar a data e hora
    data_hora_formatada = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')

    # Registrar a batida de ponto no arquivo
    with open('registro_ponto.txt', 'a') as arquivo:
        arquivo.write(data_hora_formatada + '\n')

    print('Batida de ponto registrada com sucesso.')


def registrar_ponto_clicado():
    registrar_ponto()
    status_label.config(text="Batida de ponto registrada com sucesso.")


# Criação da janela
janela = tk.Tk()
janela.title("Sistema de Batida de Ponto")
janela.geometry("300x150")

# Botão para registrar batida de ponto
botao_registrar_ponto = tk.Button(janela, text="Registrar Ponto", command=registrar_ponto_clicado)
botao_registrar_ponto.pack(pady=20)

# Rótulo para exibir o status
status_label = tk.Label(janela, text="")
status_label.pack()

# Iniciar o loop da interface gráfica
janela.mainloop()
