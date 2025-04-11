# Buscar enlaces de paginación
pagination_links = soup.find_all('a', class_='andes-pagination__link')

# Lista para almacenar las URLs de las páginas
page_urls = []

for link in pagination_links:
    href = link.get('href')  # Obtener la URL
    if href and href not in page_urls:  # Evitar duplicados
        page_urls.append(href)  # Agregar URL a la lista

# Imprimir todas las URLs de paginación encontradas
print("Enlaces de paginación encontrados:")
for url in page_urls:
    print(url)
