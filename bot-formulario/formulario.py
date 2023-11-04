import time
from datetime import date, timedelta
import keyring
from browser import *
from windows import *
from unidades import oge
import os

pasta_formularios = keyring.get_password('MGOUV', 'formularios')    # Pasta onde serão armazenados os formulários baixados
tempo_entre_tentativas = 600                                        # Tempo de espera de 10 minutos entre tentativas falhas

# Sequência de navegação do browser para login no Sistema MGOUV
sequencia_login = [['INPUT', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[1]/input', keyring.get_password('MGOUV', 'cpf')],
                   ['INPUT', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[2]/div[1]/input', keyring.get_password('MGOUV', 'senha')],
                   ['CLICK', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[4]/button[2]'],
                   ['CLICK', '/html/body/div[3]/div[2]/div/div[1]/table/tbody[1]/tr[2]/td/div']]

# Sequência de navegação do browser pós seleção de unidade
sequencia_campos_dinamicos = [['CLICK','/html/body/div[1]/div/div/div/div/div/div[1]/a'],                                     # Botão Sanduíche (Menu)
                              ['CLICK','/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/a'],             # Botão Acompanhamento
                              ['CLICK','/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/ul/li[3]/a']]    # Botão Relatório Campos Dinâmicos
                        
# Sequência de alteração de unidade
sequencia_usuario = [['CLICK', '/html/body/div[1]/div/div/div/div/div/div[1]/div[3]/ul/li[2]/a'],                       # Botão Usuário
                     ['CLICK', '/html/body/div[1]/div/div/div/div/div/div[1]/div[3]/ul/li[2]/div/ul/li[2]/div/a']]      # Botão Alterar Unidade

def bot_formulario(tentativas:int=0):
    '''
    DOCSTRING
    '''

    browser, wait = iniciar_browser()

    try:
        navegacao_browser(wait, sequencia_login)
        inicializa_biblioteca(wait, oge)
        # encerra_browser(browser)          # Remover comentário após testes
    except:
        if tentativas < 4:                  # Define a quantidade limite de tentativas de execução do código (n-1)
            encerra_browser(browser)
            print(f'Erro identificado na tentativa {tentativas + 1}. Aguardando {tempo_entre_tentativas} segundos antes de reiniciar.')
            time.sleep(tempo_entre_tentativas)
            print('Reiniciando o processo...')
            tentativas += 1
            bot_formulario(tentativas)
        else:
            encerra_browser(browser)
            print('Sistema MGOUV indisponível!')

def inicializa_biblioteca(wait, dicionario:dict):
    '''
    DOCSTRING
    '''

    contador_unidade = 1
    for unidade, valor in dicionario.items():
        navegacao_browser(wait, sequencia_usuario)

        sequencia_unidade = [['CLICK', valor['XPATH-UN']],          # Botão referente à unidade atual da navegação
                             ['WAIT', 1]]                           # Verificar possibilidade de deleção pós testes
        
        if contador_unidade > 10:
            sequencia_unidade.insert(0,['CLICK', '/html/body/div[5]/div[2]/div/div[2]/div/ul/li[4]/a'])     # Botão para troca de página de unidades
            sequencia_unidade.insert(1,['WAIT', 1])                                                         # Verificar possibilidade de deleção pós testes

        print(f'Acessando a unidade {unidade}')
        navegacao_browser(wait, sequencia_unidade)
        navegacao_browser(wait, sequencia_campos_dinamicos)

        contador_formulario = 1
        for formulario in valor['FORMULARIO']:
            sequencia_formulario = [['CLICK', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/span[2]/a'],        # Botão lupa (busca) de formulários
                                    ['WAIT', 1]]                                                                                                            # Verificar possibilidade de deleção pós testes
            
            sequencia_formulario.insert(2, ['CLICK', formulario[1]])        # Cl
            sequencia_formulario.insert(3, ['WAIT', 1])                     # Verificar possibilidade de deleção pós testes

            if contador_formulario > 10:
                sequencia_formulario.insert(2,['CLICK', '/html/body/div[4]/div/div/div[4]/div/ul/li[4]/a'])
                sequencia_formulario.insert(3,['WAIT', 1])

            print(f'Acessando o formulário {formulario[0]}')
            navegacao_browser(wait, sequencia_formulario)

            contador_formulario += 1

            # FOR LOOP DATAS
            # OBS: Possível necessidade de recarregar a página após o download do DataFrame. O clique no botão "Limpar" torna-se inútil nesse ato.
            # CRIAÇÃO DE DATAFRAME

        contador_unidade += 1

bot_formulario()