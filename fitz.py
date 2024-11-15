from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
import shutil
import fitz
import re

def check_keywords_in_pdf(pdf_path, keywords):
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text = "\b(?:{})\b".format("|".join([re.escape(frase) for frase in keywords]))
            text_instances = page.search_for(text, text=True)
            if text_instances:
                return True
    return False


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
    for i in range(2, 94):  # Ajustar o número de municípios conforme necessário
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
            try:
                proposta = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, f"/html/body/dvg-root/main/dvg-canditado-detalhe/div/div/div[2]/form/div/div[2]/div/div/mat-accordion/mat-expansion-panel[4]/mat-expansion-panel-header/span[1]"))
                )
                proposta.click()

                pdf = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, f"/html/body/dvg-root/main/dvg-canditado-detalhe/div/div/div[2]/form/div/div[2]/div/div/mat-accordion/mat-expansion-panel[4]/div/div/dvg-candidato-proposta/ol/li/div/div"))
                )
                pdf.click()
            
                time.sleep(5)
            
                # Espera o download do PDF e verifica se as palavras-chave estão presentes
                arquivos = os.listdir(download_dir)
                primeiro_pdf = next((file for file in arquivos if file.endswith(".pdf")), None)
                pdf_name = os.path.join(download_dir, primeiro_pdf)
                keywords = ["moeda social","moedas sociais", "bancos comunitários", "banco comunitário", "transferência de renda, renda"]

                if check_keywords_in_pdf(pdf_name, keywords):
                    situacao = driver.find_element(By.XPATH, "/html/body/dvg-root/main/dvg-canditado-detalhe/div/div/div[1]/dvg-candidato-header/div/div/div/div/div/div").text
                    candidato_nome = driver.find_element(By.XPATH, '//*[@id="basicInformationSection"]/div[2]/dvg-candidato-dados/div/div[1]/label[2]').text  # Ajuste o XPATH
                    with open(f"candidatos_atualizado.txt", "a") as txt_file:
                        txt_file.write(f"Candidato: {candidato_nome}  Situação: {situacao}\n")
                        
                os.remove(pdf_name)  # Apaga o PDF       
                
                driver.back()
                time.sleep(5)
            except:
              driver.back()
              time.sleep(5)  # Pausa para carregar a lista novamente      

            
          
finally:
    # Apagar e criar a pasta pdf -> limpar memoria
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
    os.makedirs(download_dir)

    driver.quit()
    
