import requests
from bs4 import BeautifulSoup

url = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"  # Cambia por la URL que desees
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Ejemplo: Encontrar todos los encabezados h1 en la página
headers = soup.find_all("main")
for header in headers:
    print(header.text)





#footers = soup.find_all("andes-pagination")
#for footer in footers:
#    print(footer.text)





from bs4 import BeautifulSoup

html = """
<ol class="ui-search-layout ui-search-layout--grid ui-search-layout--pi">
  <li class="ui-search-layout__item">
    <div class="poly-card__portada">Portada del producto 1</div>
    <div class="poly-card__content">Contenido del producto 1</div>
  </li>
  <li class="ui-search-layout__item">
    <div class="poly-card__portada">Portada del producto 2</div>
    <div class="poly-card__content">Contenido del producto 2</div>
  </li>
  <li class="ui-search-layout__item">
    <div class="poly-card__portada">Portada del producto 3</div>
    <div class="poly-card__content">Contenido del producto 3</div>
  </li>
</ol>
"""

# Parsear el HTML
soup = BeautifulSoup(html, 'html.parser')

# Encontrar el elemento padre (OL)
ol_container = soup.find('ol', class_='ui-search-layout ui-search-layout--grid ui-search-layout--pi')

# Extraer todos los elementos hijos (LI)
if ol_container:
    items = ol_container.find_all('li', class_='ui-search-layout__item')
    for item in items:
        portada = item.find('div', class_='poly-card__portada').text
        contenido = item.find('div', class_='poly-card__content').text
        print("Portada:", portada)
        print("Contenido:", contenido)
        print("---")
else:
    print("No se encontró el elemento padre.")
