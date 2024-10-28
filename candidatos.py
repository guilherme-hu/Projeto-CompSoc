from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
import shutil
import PyPDF2
import pandas as pd


# Configurações do Chrome
chrome_options = Options()
# Define o diretório de download desejado com base no local do arquivo atual
download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdf")


# Cria a pasta "pdf" se não existir
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

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


# Lista de frases-chave
key_phrases = ["Transferência de renda", "moeda social", "renda básica"]

# Lista para armazenar os resultados
results = []

try:
    # Abrir o site
    driver.get("https://divulgacandcontas.tse.jus.br/divulga/#/home")

    # Esperar que o elemento do índice (símbolo de três traços) esteja disponível e clicar nele
    menu_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".navbar-toggler"))
    )
    menu_button.click()

    # Esperar e clicar em "Eleições"
    eleicoes_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Eleições"))
    )
    eleicoes_link.click()

    # Clicar em "Eleições Municipais 2024"
    eleicoes_municipais_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.list-group:nth-child(1) > a:nth-child(1) > div:nth-child(1)"))
    )
    eleicoes_municipais_link.click()

    # Selecionar Brasil e Região
    elemento_seletor = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".row-cols-lg-6 > div:nth-child(1)"))
    )
    elemento_seletor.click()

    # Selecionar a Região Sudeste
    regiao_select = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#regiao"))
    )
    option = regiao_select.find_element(By.CSS_SELECTOR, f"option.ng-star-inserted:nth-child(6)")  # Sudeste
    option.click()

    # Escolher o estado do Rio de Janeiro
    estado = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f"span.ng-tns-c21-7:nth-child(2)"))  # Rio de Janeiro
    )
    estado.click()

    # Clicar no botão "Candidatura"
    candidatura_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/dvg-root/main/dvg-regiao/dvg-regiao-estados/div/div/div/form/div/div[2]/div/div/mat-accordion/mat-expansion-panel[3]/div/div/div/div[1]/dvg-regiao-cargo/div/div/div[2]/div/div/div/button[1]/i"))
    )
    candidatura_button.click()

    municipio_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="codigoMunicipio"]"""))
    )
    municipio_button.click()

    # Iterar através dos municípios do RJ
    for i in range(2, 94):  # Ajustar o número de municípios conforme necessário -> 2, 94
        xpath = f"/html/body/dvg-root/main/dvg-canditado-listagem/div/div/div[1]/form/div[1]/div/div[2]/div[1]/div[2]/select/option[{i}]"
        
        municipio = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        municipio.click()

        if i == 2:  # Exemplo para selecionar o cargo de prefeito
            prefeito = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/dvg-root/main/dvg-canditado-listagem/div/div/div[1]/form/div[1]/div/div[2]/div[2]/div[2]/select/option[2]"))
            )
            prefeito.click()
        
        pesquisar = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/dvg-root/main/dvg-canditado-listagem/div/div/div[1]/form/div[1]/div/div[3]/button[1]"))
        )
        pesquisar.click()

        time.sleep(3)  # Pausa para garantir que a página carregue completamente
        
        # Obtenha a lista de candidatos novamente para cada iteração
        candidatos = driver.find_elements(By.XPATH, "//*[@id='basicInformationSection']/div[2]/div[contains(@class, 'list-group ng-star-inserted')]")
        
        for j in range(1, len(candidatos) + 1):
            # Carregar a lista de candidatos novamente para evitar "stale element exception"
            candidatos = driver.find_elements(By.XPATH, "//*[@id='basicInformationSection']/div[2]/div[contains(@class, 'list-group ng-star-inserted')]")

            # Clicar no candidato com JavaScript para evitar o erro de interceptação
            candidato = candidatos[j - 1]
            driver.execute_script("arguments[0].scrollIntoView();", candidato)  # Garantir que o elemento está visível
            time.sleep(1)  # Pausa breve para garantir visibilidade do elemento


            candidato.click()
    
            # Interagir com o elemento dentro da página do candidato
            proposta = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"/html/body/dvg-root/main/dvg-canditado-detalhe/div/div/div[2]/form/div/div[2]/div/div/mat-accordion/mat-expansion-panel[4]/mat-expansion-panel-header/span[1]"))
            )
            proposta.click()

            pdf = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"/html/body/dvg-root/main/dvg-canditado-detalhe/div/div/div[2]/form/div/div[2]/div/div/mat-accordion/mat-expansion-panel[4]/div/div/dvg-candidato-proposta/ol/li/div/div"))
            )
            pdf.click()

            # Esperar o download do arquivo
            time.sleep(5)

            # # Verificar o PDF baixado
            pdf_files = [f for f in os.listdir(download_dir) if f.endswith('.pdf')]
            for pdf_file in pdf_files:
                pdf_path = os.path.join(download_dir, pdf_file)
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    num_pages = len(reader.pages)
                    text = ""
                    print(num_pages)
                    for page_num in range(num_pages):
                        page = reader.pages[page_num]
                        text += page.extract_text()

                    # Verificar se alguma das frases-chave está no texto
                    found_phrases = [phrase for phrase in key_phrases if phrase in text]
                    if found_phrases:
                        # Adicionar os resultados à lista
                        results.append({
                            "Nome do Candidato": "Nome do Candidato",  # Substitua pelo nome real do candidato
                            "Eleito": "Sim/Não",  # Substitua pela informação real se o candidato foi eleito
                            "Palavras-Chave": ", ".join(found_phrases)
                        })

            # Apagar o PDF após a leitura
            os.remove(pdf_path)

            # Voltar para a página de lista de candidatos
            driver.back()
            time.sleep(1)  # Pausa para carregar a lista novamente
          
finally:

    driver.quit()

    # Apagar e criar a pasta pdf -> limpar memoria
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)

    print (results)
    # Salvar os resultados em uma planilha
    if results:
        df = pd.DataFrame(results)
        df.to_excel("resultados.xlsx", index=False)
