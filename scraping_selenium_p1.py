from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Configurar Selenium en modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU (opcional, mejora rendimiento en algunos sistemas)
chrome_options.add_argument("--no-sandbox")  # Requerido en algunos entornos de servidor
chrome_options.add_argument("--window-size=1920,1080")  # Simular tamaño de ventana

# Ruta al ChromeDriver
service = Service("ruta/al/chromedriver")  # Cambia 'ruta/al/chromedriver' por la ubicación correcta de tu ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL de la página que deseas scrapear
url = "https://www.portalinmobiliario.com/arriendo/departamento/santiago-metropolitana"
driver.get(url)

try:
    # Obtener el HTML renderizado dinámicamente
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Encontrar el elemento padre (OL)
    ol_container = soup.find("ol", class_="ui-search-layout ui-search-layout--grid ui-search-layout--pi")

    # Verificar si existe el elemento padre
    if ol_container:
        # Extraer todos los elementos hijos (LI)
        items = ol_container.find_all("li", class_="ui-search-layout__item")

        for item in items:
            # Extraer contenido principal y buscar los datos adicionales
            contenido = item.find("div", class_="poly-card__content")

            if contenido:
                # Extraer unidades disponibles
                units = contenido.find("span", class_="poly-component__available-units")
                print("Unidades disponibles:", units.text.strip() if units else "No disponible")

                # Extraer cantidad de visitas
                cant_visitas = contenido.find("span", class_="poly-component__visit-request")
                print("Cantidad de visitas:", cant_visitas.text.strip() if cant_visitas else "No disponible")

                # Extraer otros datos (como en tu script anterior)
                tipo_arriendo = contenido.find("span", class_="poly-component__headline")
                direccion = contenido.find("a", class_="poly-component__title")
                atributos = contenido.find("ul", class_="poly-component__attributes-list")
                price_container = item.find("div", class_="poly-component__price")

                imagen = item.find("img", class_="poly-component__picture")
                imagen_src = imagen["src"] if imagen else "No disponible"

                price_fraction = None
                currency_symbol = None

                if price_container:
                    price_fraction = price_container.find("span", class_="andes-money-amount__fraction")
                    currency_symbol = price_container.find("span", class_="andes-money-amount__currency-symbol")

                print("Imagen_URL:", imagen_src)
                print("Tipo de arriendo:", tipo_arriendo.text.strip() if tipo_arriendo else "No disponible")
                print("Dirección o referencias:", direccion.text.strip() if direccion else "No disponible")
                print("Atributos:", ", ".join(attr.text.strip() for attr in atributos.find_all("li")) if atributos else "No disponible")
                print("Precio:", f"{currency_symbol.text}{price_fraction.text}" if price_container and price_fraction and currency_symbol else "No disponible")
                print("---")
    else:
        print("No se encontró el elemento padre (OL).")
finally:
    # Cerrar el navegador
    driver.quit()
