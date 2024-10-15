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

        prefeito = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/dvg-root/main/dvg-canditado-listagem/div/div/div[1]/form/div[1]/div/div[2]/div[2]/div[2]/select/option[2]"))
        )
        prefeito.click()
        
        pesquisar = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/dvg-root/main/dvg-canditado-listagem/div/div/div[1]/form/div[1]/div/div[3]/button[1]"))
        )
        pesquisar.click()


        # Localiza todos os elementos que contêm os nomes dos aux
        aux = driver.find_elements(By.XPATH, "//*[@id='basicInformationSection']/div[2]/div[contains(@class, 'list-group ng-star-inserted')]")

        time.sleep(2)  # Aguarde alguns segundos para garantir que a página carregue completamente

        # Conta o número de aux encontrados
        numero_de_aux = len(aux)

        print("Número de aux:", numero_de_aux)

        for candidato in aux:
            try:
                # Captura o nome do candidato
                nome_element = candidato.find_element(By.XPATH, ".//span[contains(@class, 'fw-bold')]")
                nome = nome_element.text

                # Captura a classe de status
                status_element = candidato.find_element(By.XPATH, ".//div[contains(@class, 'centered badge bg-danger ng-star-inserted')]")
                status = status_element.text

                print(f"Nome: {nome}, Status: {status}")
            except Exception as e:
                print(f"Erro ao processar candidato: {e}")

        # Contar quantos elementos da classe existem dentro da parte especificada
        elementos = driver.find_elements(By.XPATH, "//*[@id='basicInformationSection']/div[2]/div[contains(@class, 'list-group ng-star-inserted')]")
        numero_de_elementos = len(elementos)

        print("Número de elementos na classe especificada:", numero_de_elementos)
        # for j in range(1, numero_de_nomes+1):
        #     nome = WebDriverWait(driver, 5).until(
        #         EC.element_to_be_clickable((By.XPATH, "/html/body/dvg-root/main/dvg-canditado-listagem/div/div/div[2]/div/div/div/div/div[2]/div[{j}]/div/div/div"))
        #     )
        #     nome.click()

        #     # Faça o que você precisa depois de clicar no elemento
        #     # Por exemplo, você pode contar a quantidade de ocorrências de 'moeda social'
        #     page_text = driver.find_element(By.TAG_NAME, 'body').text
        #     word_count = page_text.lower().count("moeda social")
        #     print(f"Quantidade de ocorrências da palavra 'moeda social' na opção [{i}]: {word_count}")

finally:
    # Fechar o navegador
    driver.quit()
