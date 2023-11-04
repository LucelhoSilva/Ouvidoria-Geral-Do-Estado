'''
Este script deve ser executado apenas na primeira utilização da máquina, realizando as seguintes funções:
1 - Instalação ou atualização de pacotes necessários para execução das automações do Python.
2 - Configuração da credencial de acesso ao Sistema MGOUV.
3 - Configuração do caminho (path) no Windows para movimentação de arquivos.
'''

import subprocess
import sys

def instalador(pacote:str):
    '''
    Função para instalação do pacote Python explicitado na entrada.
    '''

    subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])     # Instala o pacote através do comando 'pip install'

pacotes = ['keyring', 'selenium']   # Pacotes que serão utilizados pelo script. Caso necessário, inclua pacotes na lista, utilizando strings.

for pacote in pacotes:              # Realiza recursão, acessando cada pacote existente na variável pacotes, do tipo list
    instalador(pacote)

import keyring

def configuracoes ():
    '''
    Função para inicializar o script de configurações.
    '''

    print('\n')
    print('#########################')
    print('##### CONFIGURAÇÕES #####')
    print('#########################\n')

    navegador_menu(menu_principal)

def navegador_menu(menu: dict):
    '''
    Função utilizada para invocar outras funções dentro do código, baseado no input do usuário.
    '''

    print('Opções disponíveis:')
    for chave in menu:
        print(f'[{chave}] - {menu[chave][0]}')
    opcao_selecionada = valida_opcao(menu)
    menu[opcao_selecionada][1]()

def valida_opcao(menu: dict) -> int:
    '''
    Função utilizada para verificar se o input do usuário atende aos valores do menu de navegação atual.
    '''

    while True:
        opcao_selecionada = input('\nDigite o número da opção desejada: ')

        try:
            opcao_selecionada = int(opcao_selecionada)
            if opcao_selecionada > len(menu) or opcao_selecionada <= 0:
                print('\nOpção inválida! Selecione apenas entre os valores disponíveis!')
            else:
                return opcao_selecionada
        except:
            print('\nEntrada inválida! Utilize apenas números inteiros positivos!')
            continue

def adiciona_credencial():
    '''
    Função utilizada para inclusão de credencial (CPF e Senha) no sistema operacional do usuário.
    OBS: Esta credencial será armazenada apenas no sistema que houve execução do código. Toda execução em sistema distinto deve solicitar nova inclusão de credenciais.
    Cabe informar ainda que esta adição será necessária apenas uma vez pro sistema utilizado pelo usuário.
    '''
    
    cpf = input('\nDigite o CPF de login no Sistema MGOUV: ')
    senha = input('Digite a senha de login no Sistema MGOUV: ')

    keyring.set_password('MGOUV', 'cpf', cpf)       # Armazena o CPF da credencial no sistema 'MGOUV', solicitado no login
    print(f'\nCredencial de acesso ao serviço MGOUV inserida com sucesso!')
    print(f'\nLogin: {cpf}')

    keyring.set_password('MGOUV', 'senha', senha)   # Armazena a Senha da credencial no sistema 'MGOUV', solicitado no login
    print(f'Senha: {senha}')

    configuracoes()

def adiciona_caminho():
    '''
    Função utilizada para inclusão dos caminhos (path) de movimentação de arquivos no sistema operacional do usuário.
    OBS: Estes caminhos serão armazenados apenas no sistema que houve execução do código. Toda execução em sistema distinto deve preceder da inclusão de seus caminhos.
    Cabe informar ainda que esta adição será necessária apenas uma vez pro sistema utilizado pelo usuário.
    '''
    
    print('Utilize o caminho (path) completo das pastas dentro do filesystem do Windows.')

    origem = input('\nDigite o caminho da pasta de origem do arquivo: ').replace('\\','/')      # Repõe todas as contrabarras do caminho por barras, evitando execução incorreta do script 
    if not origem.endswith('/'):                                                                # Verifica se o caminho se encerra com barra, adicionando-a caso contrário
        origem = origem + '/'

    destino = input('Digite o caminho da pasta de destino do arquivo: ').replace('\\','/')
    if not destino.endswith('/'):
        destino = destino + '/'

    backup = input('Digite o caminho da pasta de backup do arquivo: ').replace('\\','/')
    if not backup.endswith('/'):
        backup = backup + '/'

    keyring.set_password('MGOUV', 'origem', origem)         # Armazena o caminho da pasta de origem do arquivo (usualmente, Downloads), solicitado nas movimentações
    keyring.set_password('MGOUV', 'destino', destino)       # Armazena o caminho da pasta de destino do arquivo (pasta de extração do PowerBI), solicitado nas movimentações
    keyring.set_password('MGOUV', 'backup', backup)         # Armazena o caminho da pasta de backup de extrações, solicitado nas movimentações
    print(f'\nCaminhos atualizados com sucesso!')

    configuracoes()

def sair_programa():
    '''
    Função para finalizar a execução do programa.
    '''

    print('\nFinalizando configurações. Verifique todos os dados antes da execução do programa principal.\n')

menu_principal = {1: ('Adicionar/Atualizar Credenciais', adiciona_credencial),
                  2: ('Adicionar/Atualizar Caminhos', adiciona_caminho),
                  3: ('Sair do Programa', sair_programa)}

configuracoes()                     # Inicializa o script de configurações