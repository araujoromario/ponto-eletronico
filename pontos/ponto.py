import datetime
import time

def registrar_ponto():
    # Obter a data e hora atual
    data_hora_atual = datetime.datetime.now()
    
    # Formatar a data e hora
    data_hora_formatada = data_hora_atual.strftime('%Y-%m-%d %H:%M:%S')
    
    # Registrar a batida de ponto no arquivo
    with open('registro_ponto.txt', 'a') as arquivo:
        arquivo.write(data_hora_formatada + '\n')
    
    print('Batida de ponto registrada com sucesso.')

if __name__ == "__main__":
    while True:
        # Registrar a batida de ponto a cada hora
        agora = datetime.datetime.now()
        if agora.minute == 0:
            registrar_ponto()
        
        # Aguardar 1 minuto antes de verificar novamente
        time.sleep(60)
