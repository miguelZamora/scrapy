from selenium import webdriver
from bs4 import BeautifulSoup

# Configurar el navegador (Chrome en este caso)
driver = webdriver.Chrome()  # Asegúrate de tener el controlador de Chrome instalado
driver.get("https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana")

# Obtener el HTML renderizado dinámicamente
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Buscar los elementos dinámicos
ubicacion = soup.find('span', class_='poly-component__location')
unidades_disponibles = soup.find('span', class_='poly-component__available-units')

# Imprimir los resultados
print("Ubicación:", ubicacion.text.strip() if ubicacion else "No disponible")
print("Unidades disponibles:", unidades_disponibles.text.strip() if unidades_disponibles else "No disponible")

driver.quit()
