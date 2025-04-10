import pandas as pd
from bs4 import BeautifulSoup

html = """
<div class="categoria">
  <h2>Electrónica</h2>
  <div class="subcategoria">
    <h3>Teléfonos</h3>
    <ul>
      <li>iPhone</li>
      <li>Samsung Galaxy</li>
    </ul>
  </div>
  <div class="subcategoria">
    <h3>Computadoras</h3>
    <ul>
      <li>MacBook</li>
      <li>Dell Inspiron</li>
    </ul>
  </div>
</div>
"""

# Parsear el HTML
soup = BeautifulSoup(html, 'html.parser')

# Extraer categoría principal
categoria = soup.find('div', class_='categoria').find('h2').text

# Extraer subcategorías y elementos
datos = []
subcategorias = soup.find_all('div', class_='subcategoria')
for subcategoria in subcategorias:
    subcat_nombre = subcategoria.find('h3').text
    items = subcategoria.find_all('li')
    for item in items:
        datos.append({'Categoría': categoria, 'Subcategoría': subcat_nombre, 'Elemento': item.text})

# Crear un DataFrame de pandas
df = pd.DataFrame(datos)

# Mostrar el DataFrame
print(df)
