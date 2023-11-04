import time
from datetime import date, timedelta
import keyring
from browser import *
from windows import *
import os

arquivo_backup = str(date.today() - timedelta(days=1)) + '.csv' # Nome do arquivo CSV que irá à pasta de backup
pasta_origem = keyring.get_password('MGOUV', 'origem')          # Pasta onde o Selenium realiza o download da base de dados
pasta_destino = keyring.get_password('MGOUV', 'destino')        # Pasta onde o PowerBI realiza a extração dos dados
pasta_backup = keyring.get_password('MGOUV', 'backup')          # Pasta onde será armazenado o Backup de dados
relatorio_bi = 'Classificacao.csv'                              # Nome do arquivo utilizado pelo PowerBi para extração de dados
nome_busca = 'relatorioGeral'                                   # Nome original do arquivo baixado pelo Selenium
tentativas = 0
tempo_entre_tentativas = 600                                    # Tempo de espera de 10 minutos entre tentativas falhas

# Sequência de navegação do browser para login no Sistema MGOUV
sequencia_login = [['INPUT', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[1]/input', keyring.get_password('MGOUV', 'cpf')],
                   ['INPUT', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[2]/div[1]/input', keyring.get_password('MGOUV', 'senha')],
                   ['CLICK', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[4]/button[2]'],
                   ['CLICK', '/html/body/div[3]/div[2]/div/div[1]/table/tbody[1]/tr[2]/td/div']]

# Sequência de navegação do browser, após login no sistema, para download do arquivo CSV da Base Relatório
sequencia_relatorio = [['CLICK', '/html/body/div[1]/div/div/div/div/div/div[1]/a'],
                       ['CLICK',  '/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/a'],
                       ['CLICK',  '/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/ul/li[5]/a'],
                       ['CLICK',  '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/button[2]'],
                       ['CLICK',  '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[4]/div/div[2]/button']]

def bot_relatorio(tentativas: int):
    '''
    Função de execução principal isolada do bot de extração da Base Relatório.
    Solicita a entrada do número de tentativas para extração antes de retornar erro e encerrar a execução.
    '''
    
    browser, wait = iniciar_browser()
    try:
        navegacao_browser(wait, sequencia_login)
        navegacao_browser(wait, sequencia_relatorio)
        identifica_download(pasta_origem, nome_busca)
        if date.today().day == 1:
            renomeia_movimenta(pasta_destino, relatorio_bi, pasta_backup, arquivo_backup)       # Movimenta o arquivo de Backup referente ao mês anterior
        else:
            os.remove(pasta_destino + relatorio_bi)                                             # Caso não seja o primeiro dia do mês, exclui o arquivo da pasta de extração
        relatorio_geral = identifica_recente(pasta_origem, nome_busca)                          # Busca o arquivo CSV baixado recentemente pelo script
        renomeia_movimenta(pasta_origem, relatorio_geral, pasta_destino, relatorio_bi)          # Movimenta o arquivo atualizado à pasta de extração do PowerBI
        encerra_browser(browser)
    except:
        if tentativas < 4:                  # Define a quantidade limite de tentativas de execução do código (n-1)
            encerra_browser(browser)
            print(f'Erro identificado na tentativa {tentativas + 1}. Aguardando {tempo_entre_tentativas} segundos antes de reiniciar.')
            time.sleep(tempo_entre_tentativas)
            print('Reiniciando o processo...')
            tentativas += 1
            bot_relatorio(tentativas)
        else:
            encerra_browser(browser)
            print('Sistema MGOUV indisponível!')

bot_relatorio(tentativas)
