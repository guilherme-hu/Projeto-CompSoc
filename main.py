import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL do site
url = "https://divulgacandcontas.tse.jus.br/divulga/#/home"

# Fazendo a requisição HTTP para o site
response = requests.get(url)
response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

# Parsing do conteúdo HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Contando a quantidade de ocorrências da palavra "moeda social"
word_count = soup.get_text().lower().count("moeda social")

# Criando um DataFrame com os dados
data = {'Palavra': ['moeda social'], 'Quantidade': [word_count]}
df = pd.DataFrame(data)

# Salvando os dados em uma planilha Excel
df.to_excel('quantidade_moeda_social.xlsx', index=False)

print(f"Quantidade de ocorrências da palavra 'moeda social': {word_count}")
