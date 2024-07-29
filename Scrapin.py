from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Ejemplo de ruta del ChromeDriver
chrome_driver_path = r'C:\Users\JuanHernandez\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Configuración del WebDriver
options = Options()
options.add_argument("--headless")  # Para ejecución en modo headless (sin interfaz gráfica)
service = Service(chrome_driver_path)

# URL base de la página
base_url = 'https://www.walmart.com.gt/abarrotes?page={}'

# Número máximo de páginas que deseas analizar
numero_de_paginas = 10  # Puedes ajustar esto según tus necesidades

# Clase específica del cuadro que deseas extraer
clase_cuadro = 'vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--small pa4'

# Inicializar el WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    for pagina in range(1, numero_de_paginas + 1):
        # Construir la URL para la página actual
        url = base_url.format(pagina)
        print(f'Accediendo a la página: {url}')

        # Cargar la página con Selenium
        driver.get(url)
        time.sleep(5)  # Espera 5 segundos para que la página cargue completamente (ajustar según necesidad)

        # Obtener el contenido HTML de la página cargada
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Encontrar elementos con la clase especificada
        elementos_con_clase = soup.find_all(class_=clase_cuadro)
        print(f'Elementos encontrados en la página {pagina}: {len(elementos_con_clase)}')

        # Imprimir el contenido de los elementos encontrados
        for elemento in elementos_con_clase:
            # Extraer y mostrar el texto
            texto = elemento.find(class_='vtex-product-summary-2-x-nameContainer')
            if texto:
                print(f'Texto: {texto.get_text(strip=True)}')

            # Extraer y mostrar el precio
            precio = elemento.find(class_='vtex-store-components-3-x-priceContainer')
            if precio:
                print(f'Precio: {precio.get_text(strip=True)}')

            # Extraer y mostrar la URL de la imagen
            imagen = elemento.find(class_='vtex-product-summary-2-x-imageContainer')
            if imagen:
                img_tag = imagen.find('img')
                if img_tag and 'src' in img_tag.attrs:
                    print(f'Imagen URL: {img_tag["src"]}')

            print('-' * 80)

finally:
    # Cerrar el WebDriver al finalizar
    driver.quit()