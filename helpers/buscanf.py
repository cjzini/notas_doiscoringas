from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import streamlit as st

class Buscanf:
    def __init__(self, pasta, data_ini, data_fim):
        options = Options()
        self.download_dir = pasta
        self.data_ini = data_ini
        self.data_fim = data_fim
        # Inicia no modo invisivel
        options.add_argument("--headless")
        #options.add_argument("--start-maximized")
        options.add_experimental_option('prefs',  {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
            }
        )
        options.add_experimental_option('excludeSwitches', ['enable-logging']) # Ocultar mensagens de output
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.login_page = st.secrets["NOTAS_LOGIN"]
        self.cofre = st.secrets["NOTAS_COFRE"]
        self.usuario = st.secrets["NOTAS_USUARIO"]
        self.senha = st.secrets["NOTAS_SENHA"]
        self.wait = WebDriverWait(self.driver, 30)

    def pegarNotas(self):
        self.driver.get(self.login_page)
        txtUsuario = self.driver.find_element(By.ID, 'txtEmail')
        txtSenha = self.driver.find_element(By.ID, 'txtPassword')
        self.wait.until(EC.element_to_be_clickable(txtUsuario)).send_keys(self.usuario)
        self.wait.until(EC.element_to_be_clickable(txtSenha)).send_keys(self.senha)
        txtSenha.send_keys(Keys.ENTER)
        self.wait.until(EC.url_changes(self.login_page))  # Espera a mudança de URL após login
        self.driver.get(self.cofre)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/div[2]/div[1]/div/select')))
        selectOpcao1 = Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/div[2]/div[1]/div/select'))
        selectOpcao1.select_by_value("EmissionDate")
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/div[2]/div[1]/div/select[2]')))
        selectOpcao2 = Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/div[2]/div[1]/div/select[2]'))       
        selectOpcao2.select_by_value("$gte")
        txtData1 = self.driver.find_element(By.ID, 'txtDate1')
        txtData1.send_keys(self.data_ini)
        btnAddCampo = self.driver.find_element(By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/div[2]/div[2]/div[2]')
        btnAddCampo.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/select')))
        selectOpcao3 = Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/select'))
        selectOpcao3.select_by_value("EmissionDate")
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/select[2]')))
        selectOpcao4 = Select(self.driver.find_element(By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/select[2]'))       
        selectOpcao4.select_by_value("$lte")
        txtData2 = self.driver.find_element(By.ID, 'txtDate2')
        txtData2.send_keys(self.data_fim)
        btnBuscar = self.driver.find_element(By.ID, 'btnSearch')
        btnBuscar.click()
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="table_wrapper"]/div[1]/button[1]')))
        btnMarcarTodos = self.driver.find_element(By.XPATH, '//*[@id="table_wrapper"]/div[1]/button[1]')
        self.wait.until(EC.element_to_be_clickable(btnMarcarTodos)).click()
        # Percorrer a tabela de itens de notas fiscais e clicar na nota se esta estiver cancelada para desmarca-la
        tabela = self.driver.find_element(By.ID, 'table')
        linhas = tabela.find_elements(By.TAG_NAME, 'tr')
        # Iterar sobre as linhas
        for linha in linhas:
            try:
                # Verifique se existe um <div> com a classe e texto desejados
                div = linha.find_element(By.CLASS_NAME, "eventFormat.CMT")
                if div.text == "CMT":
                    # Clique na linha
                    linha.click()
            except Exception as e:
                # Ignorar linhas que não contêm o elemento
                pass
        time.sleep(3)
        btnBaixar = self.driver.find_element(By.XPATH, '//*[@id="ctl00"]/div[4]/div[2]/div[2]/button[1]')
        self.wait.until(EC.element_to_be_clickable(btnBaixar)).click()
        chkNumNota = self.driver.find_element(By.XPATH, '//*[@id="MainContent_cphMainContent_advancedsearch_DownloadXml_cbRenameByNumberXml"]')
        self.wait.until(EC.element_to_be_clickable(chkNumNota)).click()
        btnConfirmar = self.driver.find_element(By.XPATH, '//*[@id="MainContent_cphMainContent_advancedsearch_DownloadXml_btnDownloadSelected"]')
        self.wait.until(EC.element_to_be_clickable(btnConfirmar)).click()
        # while any((file.endswith('.crdownload') for file in os.listdir(self.download_dir))):
        #     print("Aguardando o download ser concluido...")
        #     time.sleep(0.2)
        time.sleep(15)
        self.driver.quit()