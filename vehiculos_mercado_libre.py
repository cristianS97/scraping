import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import datetime

# Obtenemos la ruta en donde se esta ejecutando el fichero
ruta = os.path.dirname(os.path.abspath(__file__))
# Url semills
url = 'https://listado.mercadolibre.cl/%s#D[A:%s]'
# Categorías de las busquedas que realizaremos
busquedas = ['auto', 'camioneta', 'moto', 'furgon']

# Listaen donde se almacenaran los resultados para luego exportar un csv
resultados = list()

# Se iteran las distintas categorías
for busqueda in busquedas:
    # Creamos la url a consultar
    data = requests.get(url % (busqueda, busqueda))
    # Se parsea el árbol para poder buscar en el
    html = BeautifulSoup(data.text)
    # Iteramos todas las listas que se encuentren
    for ol in html.find_all('ol'):
        # Iteramos todos los elementos de dichas listas
        for li in ol.find_all('li'):
            try:
                div = li.find('div')
                div = div.find('div')
                a = div.find('a')
                title = a.get('title')
                precio = li.find('span', class_='price-tag-fraction').text
                region = li.find('span', class_='ui-search-item__group__element ui-search-item__location').text
                year = li.find_all('li', class_='ui-search-card-attributes__attribute')[0].text
                km = li.find_all('li', class_='ui-search-card-attributes__attribute')[1].text
                # Creamos una lista con los elemntos buscados
                resultados.append({
                    'title': title.replace(',', ''),
                    'region': region.replace(',', ''),
                    'category': busqueda.replace(',', ''),
                    'year': year.replace(',', ''),
                    'km': km.replace(',', ''),
                    'price': precio.replace(',', '')

                })
                # Imprimimos los resultados
                print(busqueda)
                print(title)
                print(precio)
                print(region)
                print(year)
                print(km)
                print()
            except:
                pass

# Creamos el nombre del fichero
nombre = datetime.datetime.now().strftime('%d%m%Y%H%m%S') + '.csv'

# Comprobamos si existe el directorio en donde se guardarán los ficheros de busqueda
if not os.path.exists(os.path.join(ruta, 'ficheros', 'busquedas_mercado_libre')):
    os.makedirs(os.path.join(ruta, 'ficheros', 'busquedas_mercado_libre'))

# Exportamos el fichero
pd.DataFrame(resultados).to_csv(os.path.join(ruta, 'ficheros', 'busquedas_mercado_libre', nombre), index=False)

print('Fichero creado')