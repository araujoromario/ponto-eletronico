import tkinter as tk
from datetime import datetime
import pandas as pd

# Função para registrar a batida de ponto
def registrar_ponto(vigia_nome):
    # Obter a data e hora atual
    data_hora_atual = datetime.now()
    
    # Formatar a data e hora
    data_formatada = data_hora_atual.strftime('%Y-%m-%d')
    hora_formatada = data_hora_atual.strftime('%H:%M:%S')
    
    # Criar um DataFrame com os dados
    dados = pd.DataFrame({'Vigia': [vigia_nome], 'Data': [data_formatada], 'Hora': [hora_formatada]})
    
    # Salvar os dados no arquivo Excel
    nome_arquivo = f'{vigia_nome}_registro_ponto.xlsx'
    dados.to_excel(nome_arquivo, index=False)
    
    print(f'Batida de ponto registrada para {vigia_nome} em {data_formatada} às {hora_formatada}.')

# Funções para os botões
def registrar_ponto_gabriel():
    registrar_ponto("GABRIEL")

def registrar_ponto_ferreira():
    registrar_ponto("FERREIRA")

# Criação da janela
janela = tk.Tk()
janela.title("Sistema de Batida de Ponto")
janela.geometry("300x200")

# Carregar a imagem da logo da empresa
logo = tk.PhotoImage(file="img/logo.png")  # Substitua pelo caminho da sua imagem

# Exibir a logo no fundo da janela
fundo_com_logo = tk.Label(janela, image=logo)
fundo_com_logo.place(x=0, y=0, relwidth=1, relheight=1)

# Botões para registrar batida de ponto para GABRIEL e FERREIRA
botao_registrar_gabriel = tk.Button(janela, text="Registrar Ponto para GABRIEL", command=registrar_ponto_gabriel)
botao_registrar_gabriel.pack(pady=20)

botao_registrar_ferreira = tk.Button(janela, text="Registrar Ponto para JERRY", command=registrar_ponto_ferreira)
botao_registrar_ferreira.pack(pady=10)

# Iniciar o loop da interface gráfica
janela.mainloop()
