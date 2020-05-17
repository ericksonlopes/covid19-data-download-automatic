# Install
# pip install selenium

from selenium import webdriver
import os
import time
from datetime import date


class CovidCase:
    def __init__(self):
        # variavel com o nome do arquivo que armazena as datas
        self.arquivo_data = 'date.txt'
        self.pasta_arquivos = 'arquivos'

        # verifica se a pasta não existe
        if not os.path.exists(self.pasta_arquivos):
            # cria a pasta
            os.mkdir(self.pasta_arquivos)

        # verifica se o arquivo não existe
        if not os.path.exists(self.arquivo_data):
            # cria o arquivo
            open(self.arquivo_data, 'x')

        # armazena o dat atual ex:15/05/2020
        data_atual = date.today().strftime('%d%m%Y')

        # abre o arquivo
        with open(self.arquivo_data, 'r', encoding='utf-8') as file:
            # verifica se a ultima data é equivalente ao dia atual
            if data_atual not in file.read().split('\n')[-2].split(',')[0]:
                print('Data de Hoje Desatualizada')

                # executa a função que retorna a ultima atualização do site,
                # verificando se existe essa data dentro do arquivo(selenium), se não existir, pela essa parte
                if self.busca_data() not in self.busca_data_arquivo():
                    # executa a função que baixa o arquivo
                    self.baixar_novo_arquivo()
                    # salva a data atual no arquivo, acrescentando 'atualizado' por ter baixado o arquivo
                    self.salva_dados(data_atual + ',atualizado')

                # Caso a data de atualização do site seja equivalente a data atual
                else:
                    # Salva que esta desatualizado
                    self.salva_dados(data_atual + ',desatualizado')

            # se a última data for equivalente ao dia atual
            else:
                print('Data Atualizada')

    # função que salva no arquivo
    def salva_dados(self, dados):
        with open(self.arquivo_data, 'a') as arquivo:
            arquivo.write(dados + '\n')

    # função que busca data no site
    def busca_data(self):
        try:
            # diretório onde será salvo o arquivo
            download_dir = os.path.join(os.getcwd(), self.pasta_arquivos)
            # convoca a função de opções do webdriver
            self.chrome_options = webdriver.ChromeOptions()
            # modifica o lugar onde o download será enviado
            self.chrome_options.add_experimental_option("prefs",
                                                        {"download.default_directory": download_dir,
                                                         "directory_upgrade": True,
                                                         "safebrowsing.enabled": True})
            # adiciona no webdriver as opções e especifica o local do google driver 
            self.chrome = webdriver.Chrome(executable_path='webdriver/chromedriver.exe',
                                           chrome_options=self.chrome_options)
            # Site que irá abrir
            self.chrome.get('https://covid.saude.gov.br/')
        except Exception as err:
            # caso gere erro
            print(err)

        else:
            # classe onde está a data de atualização
            dados = self.chrome.find_element_by_class_name('lb-grey')
            # limpa os dados para receber apenas a data
            dados_cut = dados.text.split(' ')[1][4:].replace('/', '')
            # retorna a data recebida
            return dados_cut

    # função que baixa o arquivo
    def baixar_novo_arquivo(self):
        try:
            # caminho xpath do botão
            baixar = self.chrome.find_element_by_xpath(
                '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div['
                '1]/div[2]/ion-button')
            # clica no botão
            baixar.click()
            # Gera um tempo até o arquivo ser baixado
            time.sleep(20)

        except Exception as err:
            # caso gere erro
            print(err)

        else:
            print('Download file')

    # classe para buscar as datas dos arquivos que estão nos nomes
    def busca_data_arquivo(self):
        # lista o conteudo da pasta
        pasta_csv = os.listdir(self.pasta_arquivos)
        lista = []
        # percorre os itens encontrado
        for item in pasta_csv:
            # limpa o arquivo pegando somente a data
            cut = item.split('_')[-1].split('.')[0]
            # separa as datas em dia, mes, ano
            lista.append(cut[-2:] + cut[4:-2] + cut[:4])
        # retorna a lista com as datas nos nomes
        return lista


if __name__ == '__main__':
    # Inicia a Classe
    CovidCase()
