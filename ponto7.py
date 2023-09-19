import tkinter as tk
from datetime import datetime
import pandas as pd
import os

# Função para registrar a batida de ponto
def registrar_ponto(vigia_nome):
    # Obter a data e hora atual
    data_hora_atual = datetime.now()
    
    # Formatar a data e hora
    data_formatada = data_hora_atual.strftime('%Y-%m-%d')
    hora_formatada = data_hora_atual.strftime('%H:%M:%S')
    
    # Criar um DataFrame com os dados
    dados_novos = pd.DataFrame({'Vigia': [vigia_nome], 'Data': [data_formatada], 'Hora': [hora_formatada]})
    
    # Verificar se o arquivo Excel já existe
    if os.path.exists(f'{vigia_nome}_registro_ponto.xlsx'):
        # Carregar os dados existentes
        dados_antigos = pd.read_excel(f'{vigia_nome}_registro_ponto.xlsx')
        
        # Concatenar os dados novos com os existentes
        dados_completos = pd.concat([dados_antigos, dados_novos], ignore_index=True)
    else:
        dados_completos = dados_novos
    
    # Salvar os dados no mesmo arquivo Excel
    dados_completos.to_excel(f'{vigia_nome}_registro_ponto.xlsx', index=False)
    
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

# Definir a cor de fundo como azul claro
janela.configure(bg='#E6F0FF')

# Botões para registrar batida de ponto para GABRIEL e FERREIRA
botao_registrar_gabriel = tk.Button(janela, text="Registrar Ponto para GABRIEL", command=registrar_ponto_gabriel)
botao_registrar_gabriel.pack(pady=20)

botao_registrar_ferreira = tk.Button(janela, text="Registrar Ponto para FERREIRA", command=registrar_ponto_ferreira)
botao_registrar_ferreira.pack(pady=10)

# Iniciar o loop da interface gráfica
janela.mainloop()
