import time
from datetime import date
from browser import *
from historico import *
from relatorio import *
from sequencias import *

def bot_controlador():
    '''
    Função de execução principal dos bots.
    '''

    # Parâmetros de execução
    bots = [bot_historico, bot_relatorio]   # Lista sequencial de bots a serem executados
    tentativas = 5                          # Limite de tentativas por bot
    tempo_entre_tentativas = 600            # Tempo de espera de 10 minutos entre tentativas de execução

    execucao_inicio = time.time()           # Obter o tempo de início da execução do script
    
    browser, wait = iniciar_browser()
    navegacao_browser(wait, sequencia_login)

    for bot in bots:
        for tentativa in range(tentativas):
            try:
                print(f'\nInicializando bot {bot}.\n')
                bot(wait)
                break

            except Exception as erro:
                encerra_browser(browser)
                with open('erros.txt', 'a') as f:                                       # Abrir o arquivo de texto para escrita
                    f.write(f'{date.today()} - {bot} - Erro identificado: \n{erro}\n')  # Inserir o erro identificado no final do arquivo de texto

                print(f'Erro identificado na tentativa {tentativa + 1}. Aguardando {tempo_entre_tentativas} segundos antes de reiniciar.')
                time.sleep(tempo_entre_tentativas)

                print('Reiniciando o processo...\n')
                browser, wait = iniciar_browser()
                navegacao_browser(wait, sequencia_login)

    encerra_browser(browser)

    execucao_fim = time.time()                                                                  # Obter o tempo de término da execução do script
    execucao_total = execucao_fim - execucao_inicio                                             # Calcular o tempo total de execução do script

    with open('tempo-execucao.txt', 'a') as f:                                                  # Abrir o arquivo de texto para escrita
        f.write(f'{date.today()} - Tempo total de execução: {execucao_total:.2f} segundos\n')   # Inserir o tempo total de execução no final do arquivo de texto

bot_controlador()