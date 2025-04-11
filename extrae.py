import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import uuid

# Configurar el navegador (usando Selenium para manejar contenido dinámico)
driver = webdriver.Chrome()  # Asegúrate de tener el chromedriver compatible instalado
base_url = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"

# CARGA LA PÁGINA BASE Y EXTRAE LAS URLS DE PAGINACIÓN
driver.get(base_url)
time.sleep(10)  # Esperar a que se cargue completamente la página

# Obtener el HTML renderizado
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Extraer enlaces de paginación
pagination_links = soup.find_all('a', class_='andes-pagination__link')
page_urls = []
for link in pagination_links:
    href = link.get('href')
    if href and href not in page_urls:
        page_urls.append(href)

# Si las URLs son relativas, agregarles la base adecuada:
final_page_urls = []
for url in page_urls:
    if url.startswith('/'):
        final_page_urls.append("https://www.portalinmobiliario.com" + url)
    else:
        final_page_urls.append(url)

# Incluir la página base si no está ya en la lista
if base_url not in final_page_urls:
    final_page_urls.insert(0, base_url)

print("Listado de URLs de paginación:")
for url in final_page_urls:
    print(url)

# Opcional: Guardar el listado de URLs en un archivo de texto
with open("pagination_urls.txt", "w", encoding="utf-8") as f:
    for url in final_page_urls:
        f.write(url + "\n")

# Generar un UID para el nombre del archivo CSV
uid = uuid.uuid4()
csv_filename = 'resultados_scraping_' + str(uid) + '.csv'

# Abrir archivo CSV para almacenar los datos
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    # Definir los encabezados del CSV
    fieldnames = [
        'Tipo de arriendo', 'URL del producto', 'Vendedor', 'Precio',
        'Atributos', 'Localización', 'Solicitudes de visitas', 'Unidades disponibles'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Recorrer cada una de las URLs extraídas y realizar el scraping
    for page_url in final_page_urls:
        driver.get(page_url)
        time.sleep(10)  # Esperar a que cargue completamente la página

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Buscar el contenedor principal que contiene los registros (lista OL)
        ol_container = soup.find('ol', class_='ui-search-layout ui-search-layout--grid ui-search-layout--pi')
        if ol_container:
            items = ol_container.find_all('div', class_='ui-search-result__wrapper ui-search-result__wrapper--large')
            for item in items:
                contenido = item.find('div', class_='poly-card__content')
                if contenido:
                    # Extraer datos
                    tipo_arriendo = contenido.find('span', class_='poly-component__headline')
                    url_producto_tag = contenido.find('h3', class_='poly-component__title-wrapper')
                    url_producto = url_producto_tag.find('a')['href'] if (url_producto_tag and url_producto_tag.find('a')) else None
                    vendedor = contenido.find('span', class_='poly-component__seller')

                    precio_div = contenido.find('div', class_='poly-component__price')
                    currency_symbol = precio_div.find('span', class_='andes-money-amount__currency-symbol') if precio_div else None
                    price_fraction = precio_div.find('span', class_='andes-money-amount__fraction') if precio_div else None

                    atributos_list = contenido.find('ul', class_='poly-attributes-list')
                    atributos = [li.text.strip() for li in atributos_list.find_all('li')] if atributos_list else []

                    localizacion = contenido.find('span', class_='poly-component__location')
                    visitas = contenido.find('span', class_='poly-component__visit-request')
                    unidades_disponibles = contenido.find('span', class_='poly-component__available-units')

                    # Preparar la fila a escribir en el CSV
                    row = {
                        'Tipo de arriendo': tipo_arriendo.text.strip() if tipo_arriendo else "No disponible",
                        'URL del producto': url_producto if url_producto else "No disponible",
                        'Vendedor': vendedor.text.strip() if vendedor else "No disponible",
                        'Precio': f"{currency_symbol.text}{price_fraction.text}" if currency_symbol and price_fraction else "No disponible",
                        'Atributos': ', '.join(atributos) if atributos else "No disponible",
                        'Localización': localizacion.text.strip() if localizacion else "No disponible",
                        'Solicitudes de visitas': visitas.text.strip() if visitas else "No disponible",
                        'Unidades disponibles': unidades_disponibles.text.strip() if unidades_disponibles else "No disponible"
                    }
                    writer.writerow(row)

                    # Imprimir los datos extraídos en consola para verificación
                    print("Tipo de arriendo:", row['Tipo de arriendo'])
                    print("URL del producto:", row['URL del producto'])
                    print("Vendedor:", row['Vendedor'])
                    print("Precio:", row['Precio'])
                    print("Atributos:", row['Atributos'])
                    print("Localización:", row['Localización'])
                    print("Solicitudes de visitas:", row['Solicitudes de visitas'])
                    print("Unidades disponibles:", row['Unidades disponibles'])
                    print("---")
        else:
            print("No se encontró el contenedor principal (OL) en la página:", page_url)

driver.quit()
print("Scraping completado. Los resultados se han guardado en", csv_filename)
