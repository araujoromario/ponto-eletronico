import tkinter as tk
from datetime import datetime
import pandas as pd
import os
import requests
import cv2
from PIL import Image, ImageTk
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

# Função para criar a pasta para o vigia se não existir
def criar_pasta_vigia(vigia_nome):
    if not os.path.exists(vigia_nome):
        os.makedirs(vigia_nome)

# Função para capturar a imagem da webcam
def capturar_imagem_webcam(vigia_nome):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        # Obter a data e hora atual para nomear a imagem
        data_hora_atual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        nome_imagem = os.path.join(vigia_nome, f'{vigia_nome}_{data_hora_atual}.jpg')

        # Modificação: Criar a pasta para o vigia se não existir
        criar_pasta_vigia(vigia_nome)

        # Salvar a imagem na pasta do vigia com seu nome
        cv2.imwrite(nome_imagem, frame)
        print(f'Imagem salva como {nome_imagem}')
        return nome_imagem
    else:
        print('Erro ao capturar imagem da webcam.')
        return None

# Função para registrar a batida de ponto
def registrar_ponto(vigia_nome, imagem_path):
    hora_formatada = obter_hora_google_brasilia()
    
    if hora_formatada:
        data_formatada = datetime.now().strftime('%d-%m-%Y')
        
        # Modificação: Criar a pasta para o vigia se não existir
        criar_pasta_vigia(vigia_nome)
        
        # Modificação: Salvar o arquivo na pasta do vigia
        arquivo_path = os.path.join(vigia_nome, f'{vigia_nome}_registro_ponto.xlsx')
        
        dados_novos = pd.DataFrame({'Vigia': [vigia_nome], 'Data': [data_formatada], 'Hora': [hora_formatada]})
        
        if os.path.exists(arquivo_path):
            dados_antigos = pd.read_excel(arquivo_path)
            dados_completos = pd.concat([dados_antigos, dados_novos], ignore_index=True)
        else:
            dados_completos = dados_novos
        
        dados_completos.to_excel(arquivo_path, index=False)
        print(f'Batida de ponto registrada para {vigia_nome} em {data_formatada} às {hora_formatada}.')
        return dados_completos, imagem_path
    else:
        return None, None

# Função para registrar o ponto quando o botão é pressionado
def registrar_ponto_botao(vigia_nome, imagem_label):
    imagem_path = capturar_imagem_webcam(vigia_nome)
    if imagem_path:
        dados, _ = registrar_ponto(vigia_nome, imagem_path)
        if dados is not None:
            imagem = Image.open(imagem_path)
            imagem = imagem.resize((300, 300), Image.ANTIALIAS)
            imagem = ImageTk.PhotoImage(imagem)
            imagem_label.config(image=imagem)
            imagem_label.image = imagem

# Criação da janela
janela = tk.Tk()
janela.title("Sistema de Ponto")
janela.geometry("400x400")

# Definir a cor de fundo como azul claro
janela.configure(bg='#E6F0FF')

# Rótulo para exibir a imagem da webcam
imagem_label = tk.Label(janela, bg='#E6F0FF')
imagem_label.pack()

# Rótulo para exibir o relógio
relogio = tk.Label(janela, font=('Arial', 24), fg='black', bg='#E6F0FF')
relogio.pack(pady=20)

# Função para atualizar o relógio
def atualizar_relogio():
    hora_atual = obter_hora_google_brasilia()
    if hora_atual:
        relogio.config(text=hora_atual)
    janela.after(1000, atualizar_relogio)  # Atualiza a cada 1000 milissegundos (1 segundo)

# Botões para registrar batida de ponto para GABRIEL e FERREIRA
botao_registrar_gabriel = tk.Button(janela, text="Registrar Ponto para GABRIEL", command=lambda: registrar_ponto_botao("GABRIEL", imagem_label))
botao_registrar_gabriel.pack(pady=10)

botao_registrar_ferreira = tk.Button(janela, text="Registrar Ponto para FERREIRA", command=lambda: registrar_ponto_botao("FERREIRA", imagem_label))
botao_registrar_ferreira.pack(pady=10)

# Iniciar o loop da interface gráfica
janela.after(0, atualizar_relogio)  # Inicia a atualização do relógio
janela.mainloop()
