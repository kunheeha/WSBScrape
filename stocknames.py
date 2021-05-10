from bs4 import BeautifulSoup
import requests

source = requests.get('https://stockanalysis.com/stocks/').text

soup = BeautifulSoup(source, 'lxml')
namelist = soup.find('ul', class_='no-spacing').find_all('li')

stocknames = []

for stockname in namelist:
    stocknames.append(stockname.a.text.split(' ')[0])

print(stocknames)
