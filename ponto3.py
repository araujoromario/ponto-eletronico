import tkinter as tk
from datetime import datetime

def registrar_ponto(vigia_nome):
    # Obter a data e hora atual
    data_hora_atual = datetime.now()
    
    # Formatar a data e hora
    data_hora_formatada = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
    
    # Registrar a batida de ponto no arquivo
    with open(f'{vigia_nome}_registro_ponto.txt', 'a') as arquivo:
        arquivo.write(data_hora_formatada + '\n')
    
    print(f'Batida de ponto registrada para {vigia_nome} com sucesso.')

# Funções para os botões
def registrar_ponto_gabriel():
    registrar_ponto("GABRIEL")

def registrar_ponto_ferreira():
    registrar_ponto("FERREIRA")

# Criação da janela
janela = tk.Tk()
janela.title("Sistema de Batida de Ponto")
janela.geometry("300x200")

# Botões para registrar batida de ponto para GABRIEL e FERREIRA
botao_registrar_gabriel = tk.Button(janela, text="Registrar Ponto para GABRIEL", command=registrar_ponto_gabriel)
botao_registrar_gabriel.pack(pady=20)

botao_registrar_ferreira = tk.Button(janela, text="Registrar Ponto para FERREIRA", command=registrar_ponto_ferreira)
botao_registrar_ferreira.pack(pady=10)

# Iniciar o loop da interface gráfica
janela.mainloop()
