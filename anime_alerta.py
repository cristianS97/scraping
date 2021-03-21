import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4
import time
import random
from win10toast import ToastNotifier # pip install win10toast
import json

# URL de consulta
url = 'https://jkanime.net/'

# User-agent tor
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0'
}

# Nombres de los animes junto al día de consulta
dia = time.strftime('%A').lower()

# Lectura del fichero de configuración
with open('conf/anime_alerta/animes.json') as file:
    animes = json.load(file)

# Animes a consultar, los pasamos todos a minusculas
animes = [anime.lower() for anime in animes[dia]]
animes_encontrados = list()

# Objeto para interactuar con las notificaciones de windows
toaster = ToastNotifier()

# Ciclo que consultara hasta encontar el anime solicitado
while True:
    # Consultamos la url
    response = requests.get(url, headers=headers)
    print(f'{time.strftime("%H:%M:%S")} Estado respuesta: {response.status_code}')
    # Creamos el árbol html
    soup = BeautifulSoup(response.text)

    # Buscamos donde se encuentran los animes
    programacion = soup.find(id='slider3')
    animes_web = programacion.find_all('a', class_='odd')

    # Variable para comprobar si se encontro le anime buscado
    encontrado = False
    # Recorremos la lista de animes encontrados
    for anime_web in animes_web:
        # Obtenemos sus datos
        titulo = anime_web.find('h2').text.strip()
        episodio = anime_web.find('span', class_='episode').text.split('\n')[-1].strip()
        estreno = anime_web.find('i', class_='clock-icon').text.strip()

        # Consultamos si se encontraron los animes deseados
        for anime in animes:
            if anime.lower() in titulo.lower() and anime.lower() not in animes_encontrados:
                encontrado = True
                animes_encontrados.append(titulo.lower())
                print(titulo)
                print(episodio)
                print(estreno)
                print('=' * 80)
                print()

            if encontrado:
                # Mensaje que contiene la hora en que se encontró el anime
                mensaje = f'{time.strftime("%H:%M:%S")} -> Estrenado'
                toaster.show_toast(f'{titulo} - {episodio}', mensaje, duration=5)

            encontrado = False

    if len(animes) == len(animes_encontrados):
        break

    time.sleep(random.uniform(6.0, 8.0))

print("Fin del programa")
