import requests
from bs4 import BeautifulSoup

# URL de la página que deseas scrapear
url = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"  # Cambia por la URL real
response = requests.get(url)

# Parsear el contenido HTML
soup = BeautifulSoup(response.content, "html.parser")

# Encontrar todos los nodos padres (poly-card__content)
parent_nodes = soup.find_all('div', class_='poly-card__content')

# Iterar sobre cada nodo padre y extraer la información
for parent in parent_nodes:
    # Tipo de arriendo (headline)
    tipo_arriendo = parent.find('div', class_='poly-component__headline')
    tipo_arriendo_text = tipo_arriendo.text.strip() if tipo_arriendo else "No disponible"

    # Referencias de calles o dirección (title)
    direccion = parent.find('div', class_='poly-component__title')
    direccion_text = direccion.text.strip() if direccion else "No disponible"

    # Número de habitaciones y metros cuadrados (attributes-list)
    atributos = parent.find('ul', class_='poly-component__attributes-list')
    atributos_text = ", ".join(li.text.strip() for li in atributos.find_all('li')) if atributos else "No disponible"

    # Imprimir la información extraída
    print("Tipo de arriendo:", tipo_arriendo_text)
    print("Dirección o referencias:", direccion_text)
    print("Atributos:", atributos_text)
    print("---")
