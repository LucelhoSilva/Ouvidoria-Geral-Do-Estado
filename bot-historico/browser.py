from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def iniciar_browser():
    '''
    Função para inicialização do browser Google Chrome para execução do Selenium
    '''

    print('Inicializando browser')

    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://ouvidoria.prodemge.gov.br/mgouv-bpms-frontend/index.zul')

    wait = WebDriverWait(browser, 300)

    return browser, wait

def navegacao_browser(wait, sequencia: list):
    '''
    Função para navegação interna ao browser. Deve ser inserido dois parâmetros de entrada:
    * wait - Define o tempo de espera do navegador para verificar a disponibilidade do elemento
    * sequencia - Array bidimensional que define a sequencia de ações de navegação no browser.

    O array de sequência deve ser uma lista contendo uma lista pra cada ação à ser executada, conforme abaixo:
        * Input - ['INPUT', 'XPATH', 'DADO']
        * Click - ['CLICK', 'XPATH']
        * Limpeza - ['CLEAR', 'XPATH']
        * Espera - ['WAIT', 'SEGUNDOS']
    '''

    print('Iniciando navegação')

    for elemento in sequencia:
        if elemento[0] == 'INPUT':
            wait.until(EC.element_to_be_clickable((By.XPATH, elemento[1]))).send_keys(elemento[2])
        elif elemento[0] == 'CLICK':
            wait.until(EC.element_to_be_clickable((By.XPATH, elemento[1]))).click()
        elif elemento[0] == 'CLEAR':
            wait.until(EC.element_to_be_clickable((By.XPATH, elemento[1]))).clear()
        elif elemento[0] == 'WAIT':
            time.sleep(elemento[1])

def encerra_browser(browser):
    '''
    Função para encerrar o browser definido no parâmetro.
    '''
    
    print('Encerrando navegador')
    browser.quit()