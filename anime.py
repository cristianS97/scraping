import requests
from bs4 import BeautifulSoup

url = 'https://www3.animeflv.net/'

data = requests.get(url)

html = BeautifulSoup(data.text)

container = html.find(class_='ListEpisodios')

episodios = container.findAll('li')

print(f'Cantidad de episodios: {len(episodios)}')
print('='*30)

for i, li in enumerate(episodios):
    print(i+1)
    print(li.find('a').find('strong', class_='Title').text)
    print(li.find('a').find('span', class_='Capi').text)
    print('-'*30)