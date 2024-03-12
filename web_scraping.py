from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

url = "https://lisbonairport.com/flights/"
page = requests.get(url).text

doc = BeautifulSoup(page, 'html.parser')
departures = doc.find_all('tbody')[1]

lista = []

for flight in departures.find_all('tr'):
    l = []
    info = flight.find_all(lambda tag: tag.name == 'td' and tag.get('colspan') != '6')
    #sell_col = str(flight.find('td', class_='flight-no')).split('(')[-1].split(')')[0]

    for i in info:
        l.append(i.text)

    if l != []:
        lista += [l]

print(lista)