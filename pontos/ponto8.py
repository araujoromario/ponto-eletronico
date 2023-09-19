import tkinter as tk
from datetime import datetime
import pandas as pd
import os
import requests
import pytz

# Função para obter a hora atual de Brasília do Google
def obter_hora_google_brasilia():
    try:
        response = requests.get("http://worldtimeapi.org/api/timezone/America/Sao_Paulo")
        data = response.json()
        hora_utc = datetime.strptime(data["datetime"], '%Y-%m-%dT%H:%M:%S.%f%z')
        hora_brasilia = hora_utc.astimezone(pytz.timezone('America/Sao_Paulo'))
        hora_formatada = hora_brasilia.strftime('%H:%M:%S')
        return hora_formatada
    except requests.exceptions.RequestException as e:
        print("Erro ao obter a hora do Google:", e)
        return None

# Função para atualizar o relógio
def atualizar_relogio():
    hora_atual = obter_hora_google_brasilia()
    if hora_atual:
        relogio.config(text=hora_atual)
    janela.after(1000, atualizar_relogio)  # Atualiza a cada 1000 milissegundos (1 segundo)

# Função para registrar a batida de ponto
def registrar_ponto(vigia_nome):
    # Obter a data e hora atual de Brasília do Google
    hora_formatada = obter_hora_google_brasilia()
    
    if hora_formatada:
        # Formatar a data
        data_formatada = datetime.now().strftime('%d-%m-%Y')
        
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
janela.title("Sistema de Ponto")
janela.geometry("400x200")

# Definir a cor de fundo como azul claro
janela.configure(bg='#E6F0FF')

# Rótulo para exibir o relógio
relogio = tk.Label(janela, font=('Arial', 24), fg='black', bg='#E6F0FF')
relogio.pack(pady=20)

# Botões para registrar batida de ponto para GABRIEL e FERREIRA
botao_registrar_gabriel = tk.Button(janela, text="Registrar Ponto para GABRIEL", command=registrar_ponto_gabriel)
botao_registrar_gabriel.pack(pady=10)

botao_registrar_ferreira = tk.Button(janela, text="Registrar Ponto para FERREIRA", command=registrar_ponto_ferreira)
botao_registrar_ferreira.pack(pady=10)

# Iniciar o loop da interface gráfica
janela.after(0, atualizar_relogio)  # Inicia a atualização do relógio
janela.mainloop()
