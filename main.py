from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import PyPDF2
import os
import time
import pandas as pd

# Defina o diretório de download desejado
download_dir = os.path.join(os.path.dirname(__file__), "pdf")

keywords = ["moeda social", "outra palavra chave"]

# Configurações do Chrome
chrome_options = Options()

# Adiciona as preferências para configurar o download
prefs = {
    "download.default_directory": download_dir,
    "profile.default_content_settings.popups": 0,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
}

chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

def wait_for_download(directory, timeout=30):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = any([filename.endswith('.crdownload') for filename in os.listdir(directory)])
        seconds += 1
    return not dl_wait

def find_newest_file(directory):
    files = os.listdir(directory)
    paths = [os.path.join(directory, basename) for basename in files]
    return max(paths, key=os.path.getctime)

def read_pdf_and_search_keywords(pdf_path, keywords):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        num_pages = reader.getNumPages()
        text = ""
        for page in range(num_pages):
            text += reader.getPage(page).extract_text()
    keyword_counts = {keyword: text.lower().count(keyword.lower()) for keyword in keywords}
    return keyword_counts

try:
    # Abrir o site
    driver.get("https://divulgacandcontas.tse.jus.br/divulga/#/home")

    # Esperar que o elemento do índice (símbolo de três traços) esteja disponível e clicar nele
    menu_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".navbar-toggler"))
    )
    menu_button.click()

    # Esperar e clicar em "Eleições" -> podemos escolher as eleições de anos passados
    eleicoes_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Eleições"))
    )
    eleicoes_link.click()

    # Esperar e clicar em "Eleições Municipais 2024" usando o seletor CSS fornecido
    eleicoes_municipais_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.list-group:nth-child(1) > a:nth-child(1) > div:nth-child(1)"))
    )
    eleicoes_municipais_link.click()

    # Apertar no símbolo de Brasil
    elemento_seletor = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".row-cols-lg-6 > div:nth-child(1)"))
    )
    elemento_seletor.click()

    # Esperar e acessar o seletor CSS #regiao, com as regiões do Brasil -> possibilidade de escolher outras regiões
    regiao_select = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#regiao"))
    )

    # Clique na região Sudeste
    option = regiao_select.find_element(By.CSS_SELECTOR, f"option.ng-star-inserted:nth-child(6)") #Sudeste
    option.click()
    
    time.sleep(2)  # Aguarde alguns segundos para garantir que a página carregue completamente

    # Iterar através dos estados usando a estrutura fornecida
    estado = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"span.ng-tns-c21-{7}:nth-child(2)" )) #Rio de Janeiro
    )
    estado.click()
    
    # Apertar no botão "Candidatura"
    candidatura_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/dvg-root/main/dvg-regiao/dvg-regiao-estados/div/div/div/form/div/div[2]/div/div/mat-accordion/mat-expansion-panel[3]/div/div/div/div[1]/dvg-regiao-cargo/div/div/div[2]/div/div/div/button[1]/i"))
    )
    candidatura_button.click()

    municipio_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="codigoMunicipio"]"""))
    )
    municipio_button.click()

    municipio_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="codigoMunicipio"]"""))
    )
    municipio_button.click()

    # para todos os municipios do RJ
    for i in range(2, 94):
        # Construa o XPath dinamicamente
        xpath = f"/html/body/dvg-root/main/dvg-canditado-listagem/div/div/div[1]/form/div[1]/div/div[2]/div[1]/div[2]/select/option[{i}]"
        
        municipio = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        municipio.click()

        if i == 2:
            prefeito = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/dvg-root/main/dvg-canditado-listagem/div/div/div[1]/form/div[1]/div/div[2]/div[2]/div[2]/select/option[2]"))
            )
            prefeito.click()
        
        pesquisar = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/dvg-root/main/dvg-canditado-listagem/div/div/div[1]/form/div[1]/div/div[3]/button[1]"))
        )
        pesquisar.click()


        time.sleep(3)  # Aguarde alguns segundos para garantir que a página carregue completamente

        # Contar quantos elementos da classe existem dentro da parte especificada
        nomes = driver.find_elements(By.XPATH, "//*[@id='basicInformationSection']/div[2]/div[contains(@class, 'list-group ng-star-inserted')]")
        numero_de_nomes = len(nomes)

        for j in range(1, numero_de_nomes + 1):
            candidato = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"""//*[@id="basicInformationSection"]/div[2]/div[{i}]/div/div/div"""))
            )
            candidato.click()

            proposta = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"/html/body/dvg-root/main/dvg-canditado-detalhe/div/div/div[2]/form/div/div[2]/div/div/mat-accordion/mat-expansion-panel[4]/mat-expansion-panel-header/span[1]"))
            )
            proposta.click()

            pdf = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"/html/body/dvg-root/main/dvg-canditado-detalhe/div/div/div[2]/form/div/div[2]/div/div/mat-accordion/mat-expansion-panel[4]/div/div/dvg-candidato-proposta/ol/li/div/div"))
            )
            pdf.click()

            # Esperar até que o download seja concluído
            if wait_for_download(download_dir):
                pdf_path = find_newest_file(download_dir)
                keyword_counts = read_pdf_and_search_keywords(pdf_path, keywords)
                print(f"Palavras-chave encontradas no PDF: {keyword_counts}")
                os.remove(pdf_path)
            else:
                print("Download não concluído dentro do tempo limite.")

            driver.back()

finally:
    # Fechar o navegador
    driver.quit()
