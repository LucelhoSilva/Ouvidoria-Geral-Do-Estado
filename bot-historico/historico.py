import keyring
import time
from datetime import date, timedelta
from browser import *
from windows import *
import pandas as pd
import os

tentativas = 0
tempo_entre_tentativas = 600    # Tempo de espera de 10 minutos entre tentativas falhas
arquivo_bi = 'historico.csv'    # Nome do arquivo utilizado pelo PowerBi para extração de dados

# Sequência de navegação do browser para login no Sistema MGOUV
sequencia_login = [['INPUT', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[1]/input', keyring.get_password('MGOUV', 'cpf')],
                   ['INPUT', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[2]/div[1]/input',keyring.get_password('MGOUV', 'senha')],
                   ['CLICK', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[4]/button[2]'],
                   ['CLICK', '/html/body/div[3]/div[2]/div/div[1]/table/tbody[1]/tr[2]/td/div']]

# Sequência de navegação do browser para abertura inicial de página Relatório de Atividades
sequencia_inicial = [['CLICK', '/html/body/div[1]/div/div/div/div/div/div[1]/a'],                                     # Botão Sanduíche (Menu)                                                
                     ['CLICK', '/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/a'],             # Botão Acompanhamento
                     ['CLICK', '/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/ul/li[4]/a']]    # Botão Relatório de Atividades


def bot_historico(tentativas: int):
    '''
    Função de execução principal isolada do bot de extração da Base Histórico.
    Solicita a entrada do número de tentativas para extração antes de retornar erro e encerrar a execução.
    '''

    data_inicial = date(2019, 11, 1)                                                                    # Data inicial de pesquisa da base histórico
    data_atual = date.today()
    periodo_delta = 180                                                                                 # Limite de dias para pesquisa no Sistema MGOUV
    periodo_inicio = data_inicial                                                                       # Data inicial de busca no sistema (variável por loop)
    periodo_fim = periodo_inicio + timedelta(days=periodo_delta)                                        # Data final de busca no sistema (variável por loop)
    base = pd.DataFrame()                                                                               # Inicializa um DataFrame vazio para concatenação dos dados

    browser, wait = iniciar_browser()

    try:
        navegacao_browser(wait, sequencia_login)
        navegacao_browser(wait, sequencia_inicial)

        # Loop de verificação se a data de início da pesquisa supera a data atual (período futuro)
        while periodo_inicio <= data_atual:
            sequencia_historico = [['CLEAR', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/span[2]/input'],
                                   ['CLEAR', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/span[2]/input'],
                                   ['INPUT', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/span[2]/input',periodo_inicio.strftime("%d/%m/%Y")],
                                   ['INPUT', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/span[2]/input',periodo_fim.strftime("%d/%m/%Y")],
                                   ['CLICK', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/button[2]'],
                                   ['CLICK', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div/button']]

            
            print(f'Período pesquisado: {periodo_inicio} à {periodo_fim}')
            navegacao_browser(wait, sequencia_historico)                                                 # Realiza o download do arquivo CSV para o período pesquisado

            identifica_download(keyring.get_password('MGOUV', 'origem'), 'historico')
            arquivo_df = keyring.get_password('MGOUV', 'origem') + identifica_recente(keyring.get_password('MGOUV', 'origem'), 'historico')        # Verifica nomenclatura do arquivo baixado

            df = pd.read_csv(arquivo_df, delimiter=';', index_col='PROTOCOLO', encoding='utf_8')         # Lê o arquivo CSV baixado para o período pesquisado
            base = pd.concat([base, df])                                                                 # Concatena o arquivo atual com o DataFrame de base
            os.remove(arquivo_df)                                                                        # Deleta o arquivo baixado do sistema

            periodo_inicio = periodo_fim                                                                 # Inicia a próxima pesquisa na última data final
            periodo_fim = periodo_inicio + timedelta(days=periodo_delta)                                 # Define a data final conforme o delta estabelecido

        backup_arquivos(arquivo_bi)                                                                      # Realiza o backup do arquivo Histórico na pasta de destino, caso atenda aos requisitos
        
        base.drop_duplicates()                                                                           # Remove linhas duplicadas do DataFrame
        base.to_csv(keyring.get_password('MGOUV', 'destino') + arquivo_bi, sep=';', encoding='latin-1')  # Exporta o DataFrame para a pasta de destino com correção de caracteres (encoding)
        
        encerra_browser(browser)
        
    except Exception as erro:
        if tentativas < 4:                                                                               # Define a quantidade limite de tentativas de execução do código (n-1)
            encerra_browser(browser)
            print(f'Erro {erro} identificado na tentativa {tentativas + 1}. Aguardando {tempo_entre_tentativas} segundos antes de reiniciar.')
            time.sleep(tempo_entre_tentativas)
            print('Reiniciando o processo...')
            tentativas += 1
            bot_historico(tentativas)
        else:
            encerra_browser(browser)
            print(f'Erro {erro} identificado. Excedido o número de tentativas ({tentativas + 1}).')

bot_historico(tentativas)