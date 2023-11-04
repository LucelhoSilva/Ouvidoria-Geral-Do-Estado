import time
from datetime import date, timedelta
import keyring
from browser import *
from windows import *
from sequencias import *
import os

arquivo_backup = str(date.today() - timedelta(days=1)) + '.csv' # Nome do arquivo CSV que irá à pasta de backup
pasta_origem = keyring.get_password('MGOUV', 'origem')          # Pasta onde o Selenium realiza o download da base de dados
pasta_destino = keyring.get_password('MGOUV', 'destino')        # Pasta onde o PowerBI realiza a extração dos dados
pasta_backup = keyring.get_password('MGOUV', 'backup')          # Pasta onde será armazenado o Backup de dados
relatorio_bi = 'Classificacao.csv'                              # Nome do arquivo utilizado pelo PowerBi para extração de dados
nome_busca = 'relatorioGeral'                                   # Nome original do arquivo baixado pelo Selenium
tentativas = 0
tempo_entre_tentativas = 600                                    # Tempo de espera de 10 minutos entre tentativas falhas

def bot_relatorio(wait):
    '''
    Função de execução principal isolada do bot de extração da Base Relatório.
    Solicita a entrada do número de tentativas para extração antes de retornar erro e encerrar a execução.
    '''

    navegacao_browser(wait, sequencia_relatorio)
    identifica_download(pasta_origem, nome_busca)
    if date.today().day == 1:
        renomeia_movimenta(pasta_destino, relatorio_bi, pasta_backup, arquivo_backup)       # Movimenta o arquivo de Backup referente ao mês anterior
    else:
        os.remove(pasta_destino + relatorio_bi)                                             # Caso não seja o primeiro dia do mês, exclui o arquivo da pasta de extração
    relatorio_geral = identifica_recente(pasta_origem, nome_busca)                          # Busca o arquivo CSV baixado recentemente pelo script
    renomeia_movimenta(pasta_origem, relatorio_geral, pasta_destino, relatorio_bi)          # Movimenta o arquivo atualizado à pasta de extração do PowerBI