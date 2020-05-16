from selenium import webdriver
import os
import time
from datetime import date


class CovidCase:
    def __init__(self):
        self.arquivo_data = 'date.txt'

        if not os.path.exists('arquivos_csv'):
            os.mkdir('arquivos_csv')

        if not os.path.exists(self.arquivo_data):
            open(self.arquivo_data, 'x')

        data_atual = date.today().strftime('%d%m%Y')

        with open(self.arquivo_data, 'r', encoding='utf-8') as file:

            if data_atual not in file.read().split('\n')[-1].split(',')[0]:
                print('Data de Hoje Desatualizada')
                if self.busca_data() not in self.busca_data_arquivo():
                    self.baixar_novo_arquivo()
                    self.salva_dados(data_atual + ',atualizado')
                    for item in os.listdir('arquivos_csv'):
                        if item[-4:] == 'xlsx':
                            os.rename(f'arquivos_csv/{item}', f'arquivos_csv/{item[:-5] + ".csv"}')
                            print('achei ')

                else:
                    self.salva_dados(data_atual + ',desatualizado')
            else:
                print('Data Atualizada')

    def salva_dados(self, dados):
        with open(self.arquivo_data, 'a') as arquivo:
            arquivo.write(dados + '\n')

    def busca_data(self):

        try:
            self.chrome = webdriver.Chrome('webdriver/chromedriver.exe')
            self.chrome.get('https://covid.saude.gov.br/')
        except Exception as err:
            print(err)

        else:
            dados = self.chrome.find_element_by_class_name('lb-grey')
            dados_cut = dados.text.split(' ')[1][4:].replace('/', '')
            return dados_cut

    def baixar_novo_arquivo(self):
        try:
            self.chrome.get('https://covid.saude.gov.br/')
        except Exception as err:
            print(err)

        else:
            baixar = self.chrome.find_element_by_xpath(
                '/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div['
                '1]/div[2]/ion-button')
            baixar.click()
            time.sleep(20)
            print('Download file')

    @classmethod
    def busca_data_arquivo(cls):
        pasta_csv = os.listdir('arquivos_csv')
        lista = []

        for item in pasta_csv:
            cut = item.split('_')[-1].split('.')[0]
            lista.append(cut[-2:] + cut[4:-2] + cut[:4])
        return lista

    @classmethod
    def conf_chrome(cls):
        download_dir = os.path.join(os.getcwd(), 'arquivos_csv')
        cls.chrome_options = webdriver.ChromeOptions()
        cls.chrome_options.add_experimental_option("prefs",
                                                   {"download.default_directory": download_dir,
                                                    "directory_upgrade": True,
                                                    "safebrowsing.enabled": True})

        cls.chrome = webdriver.Chrome(executable_path='webdriver/chromedriver.exe',
                                      chrome_options=cls.chrome_options)
        return cls.chrome


if __name__ == '__main__':
    CovidCase()
