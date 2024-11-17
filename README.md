# Projeto 6 de CompSoc
MVP para Projeto Final da disciplina Computador e Sociedade, acerca do desenvolvimento de uma automação de análise de candidaturas e os temas propostos por cada político eleito

## Guia de Instalação

### Passo 1: Instalar Python

1. Acesse o site oficial do Python: [python.org](https://www.python.org/).
2. Na página inicial, clique no botão "Downloads" no menu superior.
3. Selecione a versão recomendada para o seu sistema operacional (Windows, macOS ou Linux).
4. Para usuários de Windows:
    - Clique no instalador para Windows.
    - Quando o download terminar, abra o arquivo baixado.
    - Na janela de instalação, marque a opção "Add Python to PATH" (Adicionar Python ao PATH).
    - Clique em "Install Now" (Instalar Agora) e siga as instruções na tela.
5. Para usuários de macOS:
    - Clique no instalador para macOS.
    - Quando o download terminar, abra o arquivo baixado.
    - Siga as instruções na tela para concluir a instalação.
6. Para usuários de Linux:
    - Abra o terminal.
    - Use o gerenciador de pacotes da sua distribuição para instalar o Python. Por exemplo, em distribuições baseadas no Debian, você pode usar:
        ```sh
        sudo apt-get update
        sudo apt-get install python3
        ```
7. Após a instalação, verifique se o Python foi instalado corretamente:
    - Abra o terminal (Prompt de Comando no Windows ou Terminal no macOS/Linux).
    - Digite o comando `python --version` ou `python3 --version` e pressione Enter.
    - Você deve ver a versão do Python instalada exibida no terminal.

Pronto! Agora você tem o Python instalado no seu computador.

### Passo 2: Baixar o Código

1. Você receberá uma pasta com o código do projeto. Salve essa pasta em um local de fácil acesso no seu computador, como a área de trabalho.
2. Após salvar a pasta, abra o explorador de arquivos (Windows Explorer no Windows, Finder no macOS ou o gerenciador de arquivos no Linux).
3. Navegue até o local onde você salvou a pasta do projeto.
4. Clique duas vezes na pasta para abri-la e verifique se todos os arquivos estão presentes.

Pronto! Agora você tem o código do projeto no seu computador.

### Passo 3: Instalar Bibliotecas Necessárias

1. Abra o terminal:
    - No Windows, pressione as teclas `Win + R`, digite `cmd` e pressione Enter.
    - No macOS, clique no ícone do Launchpad, digite `Terminal` na barra de busca e clique no aplicativo Terminal.
    - No Linux, pressione `Ctrl + Alt + T` ou procure por "Terminal" no menu de aplicativos.
2. Navegue até o diretório do projeto onde você salvou a pasta com o código. Para isso, use o comando `cd` seguido do caminho da pasta. Por exemplo:
    ```sh
    cd /caminho/para/a/pasta/do/projeto
    ```
    - No Windows, o caminho pode ser algo como `C:\Users\SeuUsuario\Desktop\Projeto`.
    - No macOS e Linux, o caminho pode ser algo como `/Users/SeuUsuario/Desktop/Projeto` ou `/home/SeuUsuario/Desktop/Projeto`.
3. Dentro do diretório do projeto, execute o seguinte comando para instalar todas as bibliotecas necessárias:
    ```sh
    pip install -r requirements.txt
    ```
    - Esse comando vai ler o arquivo `requirements.txt` que está na pasta do projeto e instalar todas as bibliotecas listadas nele.
4. Aguarde até que todas as bibliotecas sejam instaladas. Você verá várias mensagens no terminal enquanto as bibliotecas são baixadas e instaladas.

Pronto! Agora todas as bibliotecas necessárias estão instaladas no seu computador.

### Passo 4: Executar o Projeto

1. Certifique-se de que todas as bibliotecas necessárias foram instaladas conforme descrito no Passo 3.
2. Abra o terminal novamente:
    - No Windows, pressione as teclas `Win + R`, digite `cmd` e pressione Enter.
    - No macOS, clique no ícone do Launchpad, digite `Terminal` na barra de busca e clique no aplicativo Terminal.
    - No Linux, pressione `Ctrl + Alt + T` ou procure por "Terminal" no menu de aplicativos.
3. Navegue até o diretório do projeto onde você salvou a pasta com o código. Para isso, use o comando `cd` seguido do caminho da pasta. Por exemplo:
    ```sh
    cd /caminho/para/a/pasta/do/projeto
    ```
    - No Windows, o caminho pode ser algo como `C:\Users\SeuUsuario\Desktop\Projeto`.
    - No macOS e Linux, o caminho pode ser algo como `/Users/SeuUsuario/Desktop/Projeto` ou `/home/SeuUsuario/Desktop/Projeto`.
4. Dentro do diretório do projeto, execute o seguinte comando para iniciar o projeto:
    ```sh
    python main.py
    ```
    - Esse comando vai iniciar o programa principal do projeto.
5. Aguarde enquanto o projeto é executado. Você verá várias mensagens no terminal indicando o progresso da execução.

Pronto! Agora o projeto está em execução no seu computador. Siga as instruções exibidas no terminal para interagir com o projeto.

### Passo 5: Coleta dos resultados

Quando o código terminar de rodar, serão gerados três arquivos com os resultados encontrados na busca: um arquivo em formato txt, outro em formato csv, e um terceiro em formato Excel. Os três contém os mesmos resultados salvos! Escolha o formato que preferir e acesse!
