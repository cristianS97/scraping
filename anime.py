import requests
from bs4 import BeautifulSoup

# Url semilla
url = 'https://www3.animeflv.net/'

# Data de la request realizada al sitio
data = requests.get(url)

# Parseamos la data para poder realizar busquedas
html = BeautifulSoup(data.text)

# Buscamos el div que contiene los episodios
container = html.find(class_='ListEpisodios')

# Buscamos todos los li que contienen episodios
episodios = container.findAll('li')

print(f'Cantidad de episodios: {len(episodios)}')
print('='*30)

# Se iteran todos los li para poder buscar la data
for i, li in enumerate(episodios):
    print(i+1)
    # Extraemos el titulo
    print(li.find('a').find('strong', class_='Title').text)
    # Extraemos el número de capitulo
    print(li.find('a').find('span', class_='Capi').text)
    print('-'*30)