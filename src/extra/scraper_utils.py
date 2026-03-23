"""
Utilidades para scraping de MercadoLibre
Contiene todas las funciones de extracción y parsing de datos
"""

from bs4 import BeautifulSoup
import json
import re


def extraer_productos_schema(html_content: str, pagina_actual: int) -> list:
    """
    Extrae información de productos del JSON Schema del HTML
    
    Args:
        html_content: HTML de la página
        pagina_actual: Número de la página actual
        
    Returns:
        Lista de diccionarios con información de productos
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    productos_pagina = []
    
    script_tag = soup.find('script', {'type': 'application/ld+json'})
    
    if script_tag:
        try:
            schema_data = json.loads(script_tag.string)
            if isinstance(schema_data, dict) and '@graph' in schema_data:
                productos_schema = [item for item in schema_data['@graph'] if item.get('@type') == 'Product']
                
                for idx, product in enumerate(productos_schema, 1):
                    offers = product.get('offers', {})
                    rating = product.get('aggregateRating', {})
                    
                    disponible = offers.get('availability', 'N/A')
                    if isinstance(disponible, str) and 'InStock' in disponible:
                        disponible = 'En Stock'
                    elif isinstance(disponible, str) and 'OutOfStock' in disponible:
                        disponible = 'Agotado'
                    
                    producto_info = {
                        'pagina': pagina_actual,
                        'posicion_en_pagina': idx,
                        'titulo': product.get('name', 'N/A'),
                        'marca': product.get('brand', {}).get('name', 'N/A') if isinstance(product.get('brand'), dict) else 'N/A',
                        'imagen': product.get('image', 'N/A'),
                        'precio_actual': offers.get('price', 'N/A'),
                        'moneda': offers.get('priceCurrency', 'MXN'),
                        'url': offers.get('url', 'N/A'),
                        'disponible': disponible,
                        'calificacion': rating.get('ratingValue', 'N/A'),
                        'cantidad_calificaciones': rating.get('ratingCount', 'N/A'),
                    }
                    productos_pagina.append(producto_info)
        except json.JSONDecodeError:
            print("Error al parsear JSON Schema")
    
    return productos_pagina


def mejorar_datos_dom(html_content: str, productos_pagina: list) -> list:
    """
    Extrae información adicional del DOM (precio anterior, envío, etc)
    
    Args:
        html_content: HTML de la página
        productos_pagina: Lista de productos a mejorar
        
    Returns:
        Lista de productos con información mejorada
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    poly_cards = soup.find_all('div', class_='poly-card')
    
    for i, card in enumerate(poly_cards):
        if i < len(productos_pagina):
            # Precio anterior (descuento)
            precio_anterior_span = card.find('s', class_='andes-money-amount--previous')
            if precio_anterior_span:
                precio_anterior_text = precio_anterior_span.get_text(strip=True)
                precio_anterior = re.sub(r'\D', '', precio_anterior_text)
                if precio_anterior:
                    productos_pagina[i]['precio_anterior'] = int(precio_anterior)
                    
                    try:
                        precio_actual = float(str(productos_pagina[i]['precio_actual']).replace(',', ''))
                        precio_ant = float(precio_anterior)
                        descuento_pct = round(((precio_ant - precio_actual) / precio_ant) * 100, 1)
                        productos_pagina[i]['descuento_porcentaje'] = f"{descuento_pct}%"
                    except:
                        productos_pagina[i]['descuento_porcentaje'] = 'N/A'
            
            # Descuento mostrado
            descuento_label = card.find('span', class_='poly-price__disc_label')
            if descuento_label:
                productos_pagina[i]['descuento_label'] = descuento_label.get_text(strip=True)
            
            # Envío FULL
            full_icon = card.find('svg', attrs={'aria-label': lambda x: x and 'FULL' in x})
            productos_pagina[i]['envio_full'] = 'Sí' if full_icon else 'No'
            
            # Tipo de envío
            shipping_text = card.find('div', class_='poly-component__shipping')
            if shipping_text:
                productos_pagina[i]['tipo_envio'] = shipping_text.get_text(strip=True)
            
            # Procedencia
            procedencia = card.find('span', class_='andes-visually-hidden')
            if procedencia:
                productos_pagina[i]['procedencia'] = procedencia.get_text(strip=True)
            
            # Enviado desde
            shipped_from = card.find('span', class_='poly-component__shipped-from')
            if shipped_from:
                productos_pagina[i]['enviado_desde'] = shipped_from.get_text(strip=True)
            
            # Destacado
            highlight = card.find('span', class_='poly-component__highlight')
            if highlight:
                productos_pagina[i]['destacado'] = highlight.get_text(strip=True)
            
            # Variaciones
            variations = card.find('div', class_='poly-component__variations-compacted')
            if variations:
                var_label = variations.find('span', class_='poly-variations-compacted__label')
                if var_label:
                    productos_pagina[i]['variaciones_disponibles'] = var_label.get_text(strip=True)
            
            # Vendedor
            seller = card.find('span', class_='poly-component__seller')
            if seller:
                seller_name = seller.get_text(strip=True)
                productos_pagina[i]['vendedor'] = seller_name
                if 'Tienda oficial' in str(seller):
                    productos_pagina[i]['tienda_oficial'] = 'Sí'
            
            # Cuotas
            installments = card.find('span', class_='poly-price__installments')
            if installments:
                productos_pagina[i]['cuotas'] = installments.get_text(strip=True)
    
    return productos_pagina


def obtener_siguiente_url(html_content: str) -> str:
    """
    Extrae la URL del botón "Siguiente" de la paginación
    Busca en los atributos href de los links de paginación
    
    Args:
        html_content: HTML de la página
        
    Returns:
        URL de la siguiente página o None
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Buscar nav con aria-label="Paginación"
    pagination_nav = soup.find('nav', attrs={'aria-label': 'Paginación'})
    
    if pagination_nav:
        # Buscar todos los links con clase andes-pagination__link
        pagination_links = pagination_nav.find_all('a', class_='andes-pagination__link')
        
        # El último link generalmente es "Siguiente" o podemos buscar por atributo data
        for link in pagination_links:
            href = link.get('href', '')
            # Buscar el link con control "next" o que no esté deshabilitado
            control = link.get('data-andes-pagination-control', '')
            state = link.get('data-andes-state', '')
            
            if control == 'next' and state != 'disabled' and href:
                return href
            
            # Alternativa: el penúltimo link podría ser "Siguiente"
            title = link.get('title', '')
            if 'siguiente' in title.lower() and href:
                return href
    
    return None


def exportar_a_excel(productos: list, archivo_xlsx: str) -> None:
    """
    Exporta todos los productos a un archivo Excel
    
    Args:
        productos: Lista de diccionarios con datos de productos
        archivo_xlsx: Ruta del archivo Excel a generar
    """
    import pandas as pd
    
    if not productos:
        print("No hay productos para exportar")
        return
    
    df = pd.DataFrame(productos)
    
    # Reordenar columnas de forma lógica
    columnas_orden = [
        'posicion_global', 'pagina', 'posicion_en_pagina', 'titulo', 'marca', 
        'precio_actual', 'precio_anterior', 'descuento_label', 'descuento_porcentaje', 
        'moneda', 'calificacion', 'cantidad_calificaciones', 'disponible', 
        'envio_full', 'tipo_envio', 'enviado_desde', 'cuotas', 'destacado', 
        'variaciones_disponibles', 'vendedor', 'tienda_oficial', 'procedencia', 
        'imagen', 'url'
    ]
    
    # Mantener solo las columnas que existen
    columnas_finales = [col for col in columnas_orden if col in df.columns]
    df = df[columnas_finales]
    
    # Escribir a Excel
    df.to_excel(archivo_xlsx, index=False, sheet_name='Productos')
    
    print(f"\n{'='*80}")
    print(f"✓ Datos guardados en {archivo_xlsx}")
    print(f"✓ Total de productos extraídos: {len(productos)}")
    print(f"✓ Total de páginas scrapeadas: {max([p.get('pagina', 1) for p in productos]) if productos else 0}")
    print(f"{'='*80}\n")
