from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

url = "https://www.radarbox.com/data/airports/LIS"
page = requests.get(url).text


doc = BeautifulSoup(page, 'html.parser')

print(doc)