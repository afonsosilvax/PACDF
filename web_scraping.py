from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

url = "https://lisbonairport.com/flights/"
page = requests.get(url).text

doc = BeautifulSoup(page, 'html.parser')
departures = doc.find_all('tbody')[1]

for flight in departures.find_all('tr'):
    info = flight.find_all('td')
    #sell_col = str(flight.find('td', class_='flight-no')).split('(')[-1].split(')')[0]
    print(info)
