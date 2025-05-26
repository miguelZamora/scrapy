from bs4 import BeautifulSoup
from selenium import webdriver
import time
import requests

urls = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"  # Cambia por la URL que desees


def get_urls(url):
    response = requests.get(url)
    # Obtener el HTML renderizado

    #soup = BeautifulSoup(html, 'html.parser')
    soup = BeautifulSoup(response.content, "html.parser")

    # Extraer los enlaces de paginación
    pagination_links = soup.find_all('a', class_='andes-pagination__link')
    page_urls = []

    for link in pagination_links:
        href = link.get('href')
        if href and href not in page_urls:
            page_urls.append(href)

    # Si las URLs son relativas, agregarles la base adecuada
    final_page_urls = []
    for url in page_urls:
        if url.startswith('/'):
            final_page_urls.append("https://www.portalinmobiliario.com" + url)
        else:
            final_page_urls.append(url)

    # Imprimir el listado de URLs de paginación
    print("Listado de URLs de paginación:")
    for url in final_page_urls:
        print(url)

    # Opcional: Guardar las URLs en un archivo de texto
    with open("pagination_urls.txt", "w", encoding="utf-8") as f:
        for url in final_page_urls:
            f.write(url + "\n")




get_urls(urls)