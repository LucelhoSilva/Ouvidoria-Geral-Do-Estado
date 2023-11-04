import keyring

sequencia_login = [['INPUT', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[1]/input', keyring.get_password('MGOUV', 'cpf')],              # Inserir o CPF
                   ['INPUT', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[2]/div[1]/input', keyring.get_password('MGOUV', 'senha')],     # Inserir a Senha
                   ['CLICK', '/html/body/div[1]/div/div/div[1]/div[3]/div[3]/div/div[2]/div/form/div[4]/button[2]'],                                                # Clicar no botão Entrar
                   ['CLICK', '/html/body/div[3]/div[2]/div/div[1]/table/tbody[1]/tr[2]/td/div']]                                                                    # Selecionar a unidade Ouvidoria-Geral do Estado

sequencia_relatorio = [['CLICK', '/html/body/div[1]/div/div/div/div/div/div[1]/a'],                                                                                 # Botão Sanduíche (Menu)
                       ['CLICK',  '/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/a'],                                                        # Botão Acompanhamento
                       ['CLICK',  '/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/ul/li[5]/a'],                                               # Botão Relatório Geral
                       ['WAIT', 1],                                                                                                                                 # Aguarda 1 segundo para carregar a página
                       ['CLICK',  '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/button[2]'],                                          # Botão Pesquisar
                       ['CLICK',  '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[4]/div/div[2]/button']]                    # Botão Exportar

sequencia_atividades = [['CLICK','/html/body/div[1]/div/div/div/div/div/div[1]/a'],                                                                                 # Botão Sanduíche (Menu)
                        ['CLICK','/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/a'],                                                         # Botão Acompanhamento
                        ['CLICK','/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div/div/ul/li[5]/ul/li[4]/a']]                                                # Botão Relatório de Atividades

sequencia_historico = [['CLEAR', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/span[2]/input'],                         # Limpa o campo de data inicial
                       ['CLEAR', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/span[2]/input'],                         # Limpa o campo de data final
                       ['INPUT', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/span[2]/input', "Periodo Início"],       # Insere a data inicial
                       ['INPUT', '/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/span[2]/input', "Período Fim"],          # Insere a data final
                       ['CLICK','/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div/button[2]'],                                            # Botão Pesquisar
                       ['CLICK','/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/div/button']]                                        # Botão Exportar