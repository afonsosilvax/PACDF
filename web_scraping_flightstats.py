from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# pega a versao correta do chromedriver  
servico = Service(ChromeDriverManager().install())

# abrir navegador 
navegador = webdriver.Chrome(service=servico)

# buscar url  
navegador.get("https://www.flightradar24.com/data/airports/lis/departures")

time.sleep(2)

# clicar em cookies 
navegador.find_element('xpath', '//*[@id="onetrust-accept-btn-handler"]').click()


# botao no site para exibir voos mais antigos
botao = navegador.find_element('xpath', '//*[@id="cnt-data-content"]/div/div[2]/div/aside/div[1]/table/thead/tr[2]/td/button')

# rolar até o botao (se nao aparecer anuncio, nao precisa)
ActionChains(navegador).scroll_to_element(botao).perform()

time.sleep(2)

# clicar 4 vezes, para aparecer pelo menos as ultimas 24h
i=0
while i < 4:
    botao.click()
    time.sleep(3)
    i+=1
    

# pegar o horario em que o codigo roda 
agora = datetime.datetime.now()    

# pegar o html da pagina
html = navegador.page_source

# ler o html com o beautifulsoup
soup = BeautifulSoup(html, 'html')

# tabela no html onde quero pegar os dados
tabela_voos = soup.find("table", class_="table table-condensed table-hover data-table m-n-t-15") # tabela dos voos no html


#buscando os titulos da tabela
titulos_tabela = []
for th in tabela_voos.find("tr"):  # passa por todas as tag 'th' dentro da tag 'tr', cada 'th' contem os titulos
    titulos_tabela.append(th)  # adiciona na lista vazia
    conteudo_titulos = [tag.text for tag in titulos_tabela] # pega o conteudo (.text) para cada tag 'th'
    
#nota: o ".text" serve para pegar os dados que estao escritos em forma de texto dentro de uma tag html

# criando um dataframe somente com os titulos    
df_voos = pd.DataFrame(columns=conteudo_titulos) # passando para um dataframe

# buscando as linhas da tabela
# "body" da tabela voos, onde contem as linhas da tabela
body_tabela_voos = tabela_voos.find("tbody")

# encontra todos as tag 'tr', cada 'tr' é uma linha da tabela
linhas_tabela = body_tabela_voos.find_all("tr")
linhas_tabela = linhas_tabela[2:] # este nao precisa


# pegando os dados de cada linha do html da tabela e adicionando no df os dados a cada iteracao

for linha in linhas_tabela:
    conteudo = linha.find_all("td") # cada tag 'td' é um conteudo dentro de cada linha (hora, airline, etc..)
    dados_linhas = [dados.text for dados in conteudo] # a cada iteraçao cria uma lista com os dados (.text) do conteudo
    if len(dados_linhas) != len(df_voos.columns): # isto é so para nao dar erro caso a lista nao tiver o tamanho do df
        continue
        
    df_voos.loc[len(df_voos)] = dados_linhas  # adiciona a cada iteraçao a lista "dados_linhas" no dataframe

df_voos

# passar para o excel o dataframe pronto

data_hoje = agora.strftime("%d/%m")
nome = data_hoje.replace('/', '-')
#with pd.ExcelWriter("G:\\O meu disco\\FACULDADE\\3 ANO 2 SEMESTRE\\Projeto Final Aplicado em CD\\lisboa.xlsx") as writer:
    #df_voos.to_excel(writer, sheet_name=nome, index=False) 

with pd.ExcelWriter("G:\\O meu disco\\FACULDADE\\3 ANO 2 SEMESTRE\\Projeto Final Aplicado em CD\\lisboa.xlsx",
                   mode='a') as writer:
    df_voos.to_excel(writer, sheet_name=nome, index=False)


