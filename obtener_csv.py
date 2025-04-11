import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import uuid


# Configurar el navegador (usando Selenium para manejar contenido dinámico)
driver = webdriver.Chrome()  # Asegúrate de tener el controlador compatible con tu navegador instalado
driver.get("https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana")
time.sleep(10)  # Esperar para que el contenido cargue completamente

# Obtener el HTML renderizado dinámicamente
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


uid =   uuid.uuid4()


# Crear y abrir archivo CSV para almacenar los datos
with open('resultados_scraping'+str(uid)+'.csv', 'w', newline='', encoding='utf-8') as csvfile:
    # Definir los encabezados del archivo CSV
    fieldnames = [
        'Tipo de arriendo', 'URL del producto', 'Vendedor', 'Precio',
        'Atributos', 'Localización', 'Solicitudes de visitas', 'Unidades disponibles'
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()  # Escribir la fila de encabezados

    # Buscar la lista principal que contiene los elementos (OL)
    ol_container = soup.find('ol', class_='ui-search-layout ui-search-layout--grid ui-search-layout--pi')

    if ol_container:
        # Extraer los elementos (LI) individuales
        items = ol_container.find_all('div', class_='ui-search-result__wrapper ui-search-result__wrapper--large')

        for item in items:
            # Dentro de cada LI, buscar el contenido principal
            contenido = item.find('div', class_='poly-card__content')

            if contenido:
                # Tipo de arriendo
                tipo_arriendo = contenido.find('span', class_='poly-component__headline')

                # URL del producto
                url_producto = contenido.find('h3', class_='poly-component__title-wrapper').find('a')['href']

                # Vendedor
                vendedor = contenido.find('span', class_='poly-component__seller')

                # Precio
                precio_div = contenido.find('div', class_='poly-component__price')
                currency_symbol = precio_div.find('span', class_='andes-money-amount__currency-symbol')
                price_fraction = precio_div.find('span', class_='andes-money-amount__fraction')

                # Atributos (arreglo dentro de poly-component__attributes-list)
                atributos_list = contenido.find('ul', class_='poly-attributes-list')
                atributos = [li.text.strip() for li in atributos_list.find_all('li')] if atributos_list else []

                # Localización
                localizacion = contenido.find('span', class_='poly-component__location')

                # Solicitudes de visitas
                visitas = contenido.find('span', class_='poly-component__visit-request')

                # Cantidad de departamentos
                unidades_disponibles = contenido.find('span', class_='poly-component__available-units')

                # Preparar el diccionario para escribir al archivo CSV
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

                # Escribir fila en el CSV
                writer.writerow(row)

                # Imprimir los datos extraídos
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
        print("No se encontró el contenedor principal (OL).")

# Cerrar el navegador
driver.quit()
