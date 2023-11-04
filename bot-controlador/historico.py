import keyring
from datetime import date, timedelta
from browser import *
from windows import *
from sequencias import *
import pandas as pd
import os

arquivo_historico = 'historico.csv'    # Nome do arquivo utilizado pelo PowerBi para extração de dados

def bot_historico(wait):
    '''
    Função de execução principal isolada do bot de extração da Base Histórico.
    Solicita a entrada do número de tentativas para extração antes de retornar erro e encerrar a execução.
    '''

    data_inicial = date(2019, 11, 1)                                    # Data inicial de pesquisa da base histórico
    data_atual = date.today()
    periodo_delta = 180                                                 # Limite de dias para pesquisa no Sistema MGOUV
    periodo_inicio = data_inicial                                       # Data inicial de busca no sistema (variável por loop)
    periodo_fim = periodo_inicio + timedelta(days=periodo_delta)        # Data final de busca no sistema (variável por loop)
   
    base = pd.DataFrame()                                               # Inicializa um DataFrame vazio para concatenação dos dados
    
    navegacao_browser(wait, sequencia_atividades)

    # Loop de verificação se a data de início da pesquisa supera a data atual (período futuro)
    while periodo_inicio <= data_atual:
        print(f'Período pesquisado: {periodo_inicio} à {periodo_fim}')

        sequencia_historico[2][2] = periodo_inicio.strftime("%d/%m/%Y")    # Atualiza a data inicial no sequenciamento de ações
        sequencia_historico[3][2] = periodo_fim.strftime("%d/%m/%Y")       # Atualiza a data final no sequenciamento de ações
        navegacao_browser(wait, sequencia_historico)                       # Realiza o download do arquivo CSV para o período pesquisado

        identifica_download(keyring.get_password('MGOUV', 'origem'), 'historico')
        arquivo_df = keyring.get_password('MGOUV', 'origem') + identifica_recente(keyring.get_password('MGOUV', 'origem'), 'historico')        # Verifica nomenclatura do arquivo baixado

        df = pd.read_csv(arquivo_df, delimiter=';', index_col='PROTOCOLO', encoding='utf_8')    # Lê o arquivo CSV baixado para o período pesquisado
        base = pd.concat([base, df])                                                            # Concatena o arquivo atual com o DataFrame de base
        os.remove(arquivo_df)                                                                   # Deleta o arquivo baixado do sistema

        periodo_inicio = periodo_fim                                        # Inicia a próxima pesquisa na última data final
        periodo_fim = periodo_inicio + timedelta(days=periodo_delta)        # Define a data final conforme o delta estabelecido

    backup_arquivos(arquivo_historico)     # Realiza o backup do arquivo Histórico na pasta de destino, caso atenda aos requisitos
    
    base.drop_duplicates()                                                                              # Remove linhas duplicadas do DataFrame
    base.to_csv(keyring.get_password('MGOUV', 'destino') + arquivo_historico, sep=';', encoding='latin-1')     # Exporta o DataFrame para a pasta de destino com correção de caracteres (encoding)