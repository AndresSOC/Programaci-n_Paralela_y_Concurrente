from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from scipy.stats import uniform

from scraper_utils import extraer_productos_schema, mejorar_datos_dom, obtener_siguiente_url, exportar_a_excel

# Asegurar que existe la carpeta data
import os
os.makedirs("data", exist_ok=True)

lista_productos = (
    "LENOVO-IDEAPAD-1-15AD7-15AMN7",
    "LENOVO-IDEAPAD-5-15IIL05-ALC05",
    "HP-PAVILLION-15CW-15CS",
    "HP-PAVILLION-15CX",
    "DELL-INSPIRON-3510-3511-3515-3520-3521",
    "DELL-LATITUDE-E3520-3520"
)

login_url = 'https://www.mercadolibre.com.mx'

# Configurar opciones de Chrome para evitar detección
chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--start-maximized')

# Inicializar Selenium con Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.set_page_load_timeout(30)

# Lista para almacenar todos los productos de todas las páginas
todos_los_productos = []

try:
    # Primero, ir a la página de login para que el usuario inicie sesión
    print("\n" + "="*80)
    print("PASO 1: Iniciando sesión en MercadoLibre")
    print("="*80)
    print(f"Abriendo: {login_url}")
    driver.get(login_url)
    time.sleep(3)
    
    # Esperar a que el usuario complete el login manualmente
    print("\n" + "="*80)
    print("⏳ ESPERANDO LOGIN MANUAL")
    print("="*80)
    print("Por favor, inicia sesión en la ventana de Chrome que se abrió.")
    print("Una vez que hayas iniciado sesión y estés en la página principal,")
    print("presiona ENTER en esta consola para continuar con el scraping...")
    print("="*80 + "\n")
    
    input("Presiona ENTER cuando hayas completado el login: ")
    
    print("\n✓ Login completado. Continuando con el scraping...\n")
    time.sleep(2)
    
    # Iterar sobre cada producto en la lista
    for idx_producto, nombre_producto in enumerate(lista_productos, 1):
        print("\n" + "#"*80)
        print(f"PRODUCTO {idx_producto}/{len(lista_productos)}: {nombre_producto}")
        print("#"*80 + "\n")
        
        pagina_actual = 1
        
        # Construir URL para este producto
        url_inicial = f'https://listado.mercadolibre.com.mx/Carcasa-{nombre_producto}'
        print(f"Abriendo URL de búsqueda: {url_inicial}")
        driver.get(url_inicial)
        time.sleep(5)  # Esperar a que cargue completamente
        print(f"URL actual después de cargar: {driver.current_url}\n")
        
        while True:
            print(f"\n{'='*80}")
            print(f"Scrapeando página {pagina_actual}...")
            print(f"URL: {driver.current_url}")
            print(f"{'='*80}\n")
            
            # Esperar que carguen los productos
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "poly-card"))
            )
            
            # Obtener HTML de la página actual
            html_content = driver.page_source
            
            # Guardar HTML de cada página
            html_file = f"data/mercadolibre_{nombre_producto}_pagina_{pagina_actual}.html"
            with open(html_file, "w", encoding="utf-8") as file:
                file.write(html_content)
            print(f"✓ HTML guardado en {html_file}")
            
            # Extraer productos usando funciones del módulo scraper_utils
            productos_pagina = extraer_productos_schema(html_content, pagina_actual)
            productos_pagina = mejorar_datos_dom(html_content, productos_pagina)
            
            print(f"Total de productos en página {pagina_actual}: {len(productos_pagina)}")
            
            # Agregar productos de esta página a la lista total
            todos_los_productos.extend(productos_pagina)
            
            # Buscar el botón "Siguiente" directamente con Selenium
            siguiente_url = None
            try:
                # Buscar el link de página actual para saber qué página estamos
                current_page_link = driver.find_element(By.CSS_SELECTOR, 'a[data-andes-state="selected"]')
                pagina_numero = int(current_page_link.text.strip())
                siguiente_pagina_numero = pagina_numero + 1
                print(f"Página actual detectada: {pagina_numero}, siguiente será: {siguiente_pagina_numero}")
                
                # Buscar el link de la siguiente página por número
                try:
                    next_page_link = driver.find_element(By.XPATH, f'//a[text()="{siguiente_pagina_numero}"]')
                    print(f"Botón para página {siguiente_pagina_numero} encontrado")
                    
                    # Hacer click con JavaScript en lugar de usar href
                    driver.execute_script("arguments[0].click();", next_page_link)
                    siguiente_url = "clicked"  # Indicar que se hizo click
                    
                    # Esperar a que cargue la nueva página
                    time.sleep(2)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "poly-card"))
                    )
                    print(f"Nueva página cargada")
                    
                except Exception as e:
                    print(f"No se encontró botón para página {siguiente_pagina_numero}: {e}")
                    siguiente_url = None
            except Exception as e:
                print(f"Error al buscar siguiente página: {e}")
                siguiente_url = None
            
            # Si no hay siguiente página, pasar al siguiente producto
            if not siguiente_url:
                print(f"\n✓ No hay más páginas para este producto. Continuando con el siguiente...\n")
                break
            
            # Generar delay aleatorio entre 15 y 40 segundos
            delay = uniform.rvs(loc=15, scale=25)  # loc=15, scale=25 -> [15, 40)
            print(f"Esperando {delay:.2f} segundos antes de la siguiente página...")
            time.sleep(delay)
            
            # Ya se hizo click en la siguiente página, solo incrementar contador
            pagina_actual += 1

finally:
    driver.quit()

print("\n" + "="*80)
print("✓ SCRAPING COMPLETADO")
print("="*80)
print(f"Total de productos scrapeados: {len(todos_los_productos)}")
print("="*80 + "\n")

# Agregar número global a cada producto
for i, producto in enumerate(todos_los_productos, 1):
    producto['posicion_global'] = i

# Exportar a Excel
xlsx_file = "data/productos_mercadolibre_completo.xlsx"
exportar_a_excel(todos_los_productos, xlsx_file)