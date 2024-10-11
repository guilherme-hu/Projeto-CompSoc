from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Configuração do driver (certifique-se de ter o chromedriver instalado e no PATH)
driver = webdriver.Chrome()

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

    # Esperar e clicar em "Eleições Municipais 2024" usando o seletor CSS fornecido
    eleicoes_municipais_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.list-group:nth-child(1) > a:nth-child(1) > div:nth-child(1)"))
    )
    eleicoes_municipais_link.click()

    # Esperar e clicar no seletor CSS .row-cols-lg-6 > div:nth-child(1)
    elemento_seletor = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".row-cols-lg-6 > div:nth-child(1)"))
    )
    elemento_seletor.click()

    # Esperar e acessar o seletor CSS #regiao
    regiao_select = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#regiao"))
    )

    option = regiao_select.find_element(By.CSS_SELECTOR, f"option.ng-star-inserted:nth-child(6)") #Sudeste
    option.click()
    
    time.sleep(5)  # Aguarde alguns segundos para garantir que a página carregue completamente

    # Iterar através dos estados usando a estrutura fornecida
    estado_selector = f"span.ng-tns-c21-{127}:nth-child(2)"
    estado = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, estado_selector))
    )
    estado.click()
    
    # Clicar no botão "Candidaturas" baseado no texto interno
    candidatura_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Candidaturas')]"))
    )
    candidatura_button.click()
    
    time.sleep(10)  # Aguarde alguns segundos para garantir que a página carregue completamente
    
    # Fazer a busca de palavra chave após selecionar a opção
    page_text = driver.find_element(By.TAG_NAME, 'body').text
    word_count = page_text.lower().count("moeda social")

    # Printar a quantidade de ocorrências da palavra 'moeda social' para cada estado
    print(f"Quantidade de ocorrências da palavra 'moeda social' no estado Rio de Janeiro: {word_count}")

finally:
    # Fechar o navegador
    driver.quit()
