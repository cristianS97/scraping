import requests # pip install requests
from bs4 import BeautifulSoup # pip install beautifulsoup4
import time
import random
from win10toast import ToastNotifier # pip install win10toast
import json

# Función para scrapear jkanime
def scrap_jk(anime_web):
    titulo = anime_web.find('h5').text.strip()
    episodio = anime_web.find('h6').text.strip().replace(' ', '').replace('\n', ' ')

    return titulo, episodio

# Función para scrapear animeflv
def scrap_flv(anime_web):
    titulo = anime_web.find('strong').text
    episodio = anime_web.find('span', class_="Capi").text

    return titulo, episodio

# Función para dar el mensaje de windows
def toast_message(titulo, episodio, pagina):
    # Objeto para interactuar con las notificaciones de windows
    toaster = ToastNotifier()
    mensaje = f'{time.strftime("%H:%M:%S")} -> Estrenado\nPágina: {pagina}'
    toaster.show_toast(f'{titulo} - {episodio}', mensaje, duration=5)

# Función para mostrar el mensaje por consola
def mensaje_consola(titulo, episodio, pagina, animes_encontrados):
    animes_encontrados.append(titulo.lower())
    print(titulo)
    print(episodio)
    print(pagina)
    print('=' * 80)
    print()

if __name__ == '__main__':
    # URL de consulta
    urls = [
        'https://jkanime.net/',
        'https://www3.animeflv.net/'
    ]

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

    # Ciclo que consultara hasta encontar el anime solicitado
    while True:
        for url in urls:
            # Consultamos la url
            response = requests.get(url, headers=headers)
            print(f'{time.strftime("%H:%M:%S")} Estado respuesta: {response.status_code}')
            # Creamos el árbol html
            soup = BeautifulSoup(response.text)

            if 'jkanime' in url:
                # Buscamos donde se encuentran los animes
                programacion = soup.find('div', class_='listadoanime-home')
                animes_web = programacion.find_all('a', class_='bloqq')

                # Variable para comprobar si se encontro le anime buscado
                encontrado = False
                # Recorremos la lista de animes encontrados
                for anime_web in animes_web:
                    # Obtenemos sus datos
                    titulo, episodio = scrap_jk(anime_web)

                    # Consultamos si se encontraron los animes deseados
                    for anime in animes:
                        if anime.lower() in titulo.lower() and anime.lower() not in animes_encontrados:
                            encontrado = True
                            mensaje_consola(titulo, episodio, 'jkanime', animes_encontrados)

                        if encontrado:
                            # Mensaje que contiene la hora en que se encontró el anime
                            toast_message(titulo, episodio, 'jkanime')
                        encontrado = False
            else:
                # Buscamos donde se encuentran los animes
                programacion = soup.find('ul', class_='ListEpisodios AX Rows A06 C04 D03')
                animes_web = programacion.find_all('li')
                # Variable para comprobar si se encontro le anime buscado
                encontrado = False
                # Recorremos la lista de animes encontrados
                for anime_web in animes_web:
                    # Obtenemos sus datos
                    titulo, episodio = scrap_flv(anime_web)

                    # Consultamos si se encontraron los animes deseados
                    for anime in animes:
                        if anime.lower() in titulo.lower() and anime.lower() not in animes_encontrados:
                            encontrado = True
                            mensaje_consola(titulo, episodio, 'animeflv', animes_encontrados)

                        if encontrado:
                            # Mensaje que contiene la hora en que se encontró el anime
                            toast_message(titulo, episodio, 'animeflv')

                        encontrado = False
            time.sleep(random.uniform(3.0, 4.0))

        if len(animes) == len(animes_encontrados):
            break

print("Fin del programa")
