import requests
from bs4 import BeautifulSoup

# URL de la página que deseas scrapear
url = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"

# Realizar la solicitud a la página
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
            # Extraer ubicación
            ubicacion = item.find('span', class_='poly-component__location')
            ubicacion_text = ubicacion.text.strip() if ubicacion else "No disponible"
            print("Ubicación:", ubicacion_text)

            # Extraer unidades disponibles
            unidades_disponibles = item.find('span', class_='poly-component__available-units')
            unidades_text = unidades_disponibles.text.strip() if unidades_disponibles else "No disponible"
            print("Unidades disponibles:", unidades_text)

            print("---")
    else:
        print("No se encontró el elemento padre (OL).")
else:
    print(f"Error al realizar la solicitud. Código de estado HTTP: {response.status_code}")
