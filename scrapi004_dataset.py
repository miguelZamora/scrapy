import requests
from bs4 import BeautifulSoup




# URL de la página que deseas scrapear
url = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"  # Cambia por la URL que desees
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML de la respuesta
    soup = BeautifulSoup(response.content, "html.parser")

    # Encontrar el elemento padre (OL)
    ol_container = soup.find('ol', class_='ui-search-layout ui-search-layout--grid ui-search-layout--pi')

    # Verificar si existe el elemento padre
    if ol_container:
        # Extraer todos los elementos hijos (LI)
        items = ol_container.find_all('li', class_='ui-search-layout__item')

        for item in items:
            # Extraer la portada (si existe)
            portada     = item.find('div', class_='poly-card__portada')

            # Extraer contenido principal y buscar los datos adicionales
            contenido   = item.find('div', class_='poly-card__content')

 
            if contenido:
                # Extraer el tipo de arriendo
                tipo_arriendo = contenido.find('span', class_='poly-component__headline')
                # Extraer las referencias de dirección
                direccion = contenido.find('a', class_='poly-component__title')
                # Extraer la lista de atributos (habitaciones y metros cuadrados)
                atributos = contenido.find('ul', class_='poly-component__attributes-list')

                # Extraer datos de precio
                price_container = item.find('div', class_='poly-component__price')
                price_fraction = None
                currency_symbol = None


                imagen      = item.find('img', class_='poly-component__picture')
                imagen_src  = imagen['src'] if imagen else "No disponible"
                print("Imagen_URL:", imagen_src)

                ubicacion   = item.find('span', class_='poly-component__location')
                print("Ubicación:", ubicacion.text.strip() if ubicacion else "No disponible")


                units   = contenido.find('span', class_='poly-component__available-units')
                
                if units:
                    print("Atributos:", ", ".join(attr.text.strip() for attr in atributos.find_all('li')) if atributos else "No disponible")
                    
                    print("units", ", ".join(attr.text.strip() for attr in atributos.find_all('li')) if atributos else "No disponible") 

                cant_visitas =   contenido.find('span', class_='poly-component__visit-request')

                if cant_visitas:
                    print("cant_visitas:", cant_visitas.text.strip() if cant_visitas else "No disponible")




                if price_container:
                    price_fraction = price_container.find('span', class_='andes-money-amount__fraction')
                    currency_symbol = price_container.find('span', class_='andes-money-amount__currency-symbol')





                # Imprimir los datos extraídos
                print("Tipo de arriendo:", tipo_arriendo.text.strip() if tipo_arriendo else "No disponible")
                print("Dirección o referencias:", direccion.text.strip() if direccion else "No disponible")
                print("Atributos:", ", ".join(attr.text.strip() for attr in atributos.find_all('li')) if atributos else "No disponible")
                print("Precio:", f"{currency_symbol.text}{price_fraction.text}" if price_container and price_fraction and currency_symbol else "No disponible")
                print("---")
    else:
        print("No se encontró el elemento padre (OL).")
else:
    print(f"Error al realizar la solicitud. Código de estado HTTP: {response.status_code}")
