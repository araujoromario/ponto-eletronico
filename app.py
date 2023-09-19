from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pandas as pd
import os
import requests
import cv2
from PIL import Image, ImageTk
import pytz

app = Flask(__name__)

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

# Função para capturar a imagem da webcam
def capturar_imagem_webcam(vigia_nome):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        # Obter a data e hora atual para nomear a imagem
        data_hora_atual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        nome_imagem = os.path.join('static', f'{vigia_nome}_{data_hora_atual}.jpg')

        # Modificação: Salvar a imagem na pasta do vigia com seu nome
        cv2.imwrite(os.path.join(app.root_path, nome_imagem), frame)
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
        
        # Modificação: Salvar o arquivo na pasta do vigia
        arquivo_path = os.path.join(app.root_path, f'{vigia_nome}_registro_ponto.xlsx')
        
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

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para registrar ponto para um vigia
@app.route('/registrar_ponto/<vigia_nome>')
def registrar_ponto_route(vigia_nome):
    imagem_path = capturar_imagem_webcam(vigia_nome)
    if imagem_path:
        dados, _ = registrar_ponto(vigia_nome, imagem_path)
        if dados is not None:
            imagem = Image.open(imagem_path)
            imagem = imagem.resize((300, 300), Image.ANTIALIAS)
            imagem = ImageTk.PhotoImage(imagem)
            return render_template('registro_ponto.html', imagem=imagem, dados=dados)
    return "Erro ao registrar ponto."

if __name__ == '__main__':
    app.run(debug=True)
