import os
import time

def identifica_download(pasta_origem: str, nome_busca: str):
    '''
    Esta função varre a pasta de origem do arquivo, considerando um nome de busca para parametrização, e retorna o arquivo com a data de modificação mais atual.
    '''
        
    print('Iniciando função de identificação de download de arquivo na pasta de origem.')

    # Inicializa lista com arquivos contendo o nome_busca como string de início, exceto os arquivos com extenção de download do Chrome, e filtrando arquivos com nomes diversos.
    comprimento_inicial = len([arquivo for arquivo in os.listdir(pasta_origem) if arquivo.startswith(nome_busca) and not arquivo.endswith('.crdownload')])
    tempo_limite = 0

    while True:
        time.sleep(1)

        comprimento_atual = len([arquivo for arquivo in os.listdir(pasta_origem) if arquivo.startswith(nome_busca) and not arquivo.endswith('.crdownload')])

        if comprimento_atual > comprimento_inicial:
            print('Arquivo baixado com sucesso!')
            break

        if tempo_limite == 300:
            raise Exception
        
        tempo_limite += 1

def identifica_recente(pasta_origem: str, nome_busca: str) -> str:
    '''
    Esta função varre a pasta de origem do arquivo, considerando um nome de busca para parametrização, e retorna o arquivo com a data de modificação mais atual.
    '''
        
    print('Iniciando função de identificação de arquivo recente na pasta de origem.')

    arquivos = [arquivo for arquivo in os.listdir(pasta_origem) if arquivo.startswith(nome_busca)]                  # Inicializa lista com arquivos contendo o nome_busca como string de início, filtrando arquivos com nomes diversos.
    arquivo_recente = max(arquivos, key=lambda arquivo: os.path.getmtime(os.path.join(pasta_origem, arquivo)))      # Busca o arquivo com o maior valor de Timestamp, caracterizando o arquivo mais recente dentro da lista.

    return arquivo_recente

def renomeia_movimenta(pasta_origem: str, nome_origem: str, pasta_destino: str, nome_destino: str):
    '''
    Esta função renomeia o arquivo do nome de origem para o nome de destino, movimentando-o também da pasta de origem para a pasta de destino.
    '''
        
    print('Iniciando função renomeação e movimentação de arquivos no Sistema Operacional.')

    nome_antigo = pasta_origem + nome_origem
    nome_novo = pasta_destino + nome_destino
    os.rename(nome_antigo, nome_novo)