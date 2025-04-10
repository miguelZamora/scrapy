from selenium import webdriver
from bs4 import BeautifulSoup

url = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"
driver = webdriver.Chrome()  # Asegúrate de tener el controlador de Chrome instalado
driver.get(url)

html = driver.page_source  # Obtener el HTML renderizado dinámicamente
soup = BeautifulSoup(html, 'html.parser')

# Tu código para buscar las etiquetas sigue igual
cant_visitas = soup.find('span', class_='poly-component__visit-request')
cant_unidades = soup.find('span', class_='poly-component__available-units')

print("Cantidad de visitas:", cant_visitas.text.strip() if cant_visitas else "No disponible")
print("Cantidad de unidades disponibles:", cant_unidades.text.strip() if cant_unidades else "No disponible")

driver.quit()
