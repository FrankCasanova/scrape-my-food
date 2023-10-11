import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import asyncio
from config import *
from model import Product
import re




async def scrape_el_jamon():
    """Scrapes the El Jamón supermarket website for product information.
    Returns:
        A list of `Product` objects, containing the product title, price, and price per kilogram.
    """
    async with httpx.AsyncClient(headers=HEADERS, verify=False) as client:
        
        await client.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
        await client.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
        
        products = []
        for key in EL_JAMON_URL:
            try:
                response =  await client.get(EL_JAMON_URL[key])          
                html = response.text
                parse = HTMLParser(html)
      
                title = parse.css_first('h1.tituloProducto').text()
                price_rebajado = parse.css_first("#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-oferta > span")
                if price_rebajado:
                    price = price_rebajado.text()
                    price = re.findall(r'\d+,\d+', price)       
                else:
                    price_original = parse.css_first("#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-original > span")
                    price = price_original.text()
                    price = re.findall(r'\d+,\d+', price)
                    
                    
                price_kg = parse.css_first('div.texto-porKilo').text()
                price_kg = re.findall(r'\d+,\d+', price_kg)
                  
                product = Product(
                title=title,
                price=price[0],
                price_kg=price_kg[0]
                )
                products.append(product)
                
            except Exception as e:
                # Handle the error.
                print(f'Error scraping product: {e}')
                # Create a Product object with the `Not available` values.
                product = Product(
                    title='Not available',
                    price='Not available',
                    price_kg='Not available'
                )
                # Add the product to the list of products.
                products.append(product)
                   
        return products
        

async def scrape_dia():
    """Scrapes the Día supermarket website for product information.
    Returns:
        A list of `Product` objects, containing the product title, price, and price per kilogram.
    """

    products = []

    for key in DIA_URL:
        try:
            # Get the product page.
            response = httpx.get(DIA_URL[key], headers=HEADERS)
            # Parse the HTML.
            html = response.content.decode('utf-8')
            parser = HTMLParser(html)
            # Get the product title.
            title = parser.css_first('h1.product-title').text().strip()
            # Get the product price.
            price = parser.css_first('p.buy-box__active-price').text().strip()
            price = re.findall(r'\d+,\d+', price)
            # Get the product price per kilogram.
            price_kg = parser.css_first('p.buy-box__price-per-unit').text().strip()
            price_kg = re.findall(r'\d+,\d+', price_kg)
            # Create a Product object.
            product = Product(
                title=title,
                price=price[0],
                price_kg=price_kg[0]
            )
            # Add the product to the list of products.
            products.append(product)
        except Exception as e:
            # Handle the error.
            print(f'Error scraping product: {e}')
            # Create a Product object with the `Not available` values.
            product = Product(
                title='Not available',
                price='Not available',
                price_kg='Not available'
            )
            # Add the product to the list of products.
            products.append(product)

    return products


async def scrape_carrefour():
    """Scrapes the Carrefour supermarket website for product information.
    Returns:
        A list of `Product` objects, containing the product title, price, and price per kilogram.
    """
    products = []
    for key in CARREFOUR_URL:
        try:
            response =  httpx.get(CARREFOUR_URL[key], headers=HEADERS)
            html = response.content.decode('utf-8')
            parser = HTMLParser(html)
            title = parser.css_first('h1.product-header__name').text().strip()
            price = parser.css_first('span.buybox__price').text().strip()
            price = re.findall(r'\d+,\d+', price)
            price_kg = parser.css_first('div.buybox__price-per-unit').text().strip()
            price_kg = re.findall(r'\d+,\d+', price_kg)
            
            product = Product(
                title=title,
                price=price[0],
                price_kg=price_kg[0]
            )
            products.append(product)
        except Exception as e:
            # Handle the error.
            print(f'Error scraping product: {e}')
            # Create a Product object with the `Not available` values.
            product = Product(
                title='Not available',
                price='Not available',
                price_kg='Not available'
            )
            # Add the product to the list of products.
            products.append(product)
              
    return products

async def scrape_mercadona():
    """Scrapes the Mercadona supermarket website for product information.
    Returns:
        A list of `Product` objects, containing the product title, price, and price per kilogram.
    """
    HEADERS = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',
    }
    
    products = []

    for key in MERCADONA_URL:
        try:
            # Get the product page.
            response = httpx.get(MERCADONA_URL[key], headers=HEADERS)
            # Parse the JSON response.
            data = response.json()
            # Get the product title.
            title = data['display_name']
            # Get the product price.
            price = data['price_instructions']['unit_price']
            # Get the product price per kilogram.
            price_kg = data['price_instructions']['bulk_price']
            # Create a Product object.
            product = Product(
                title=title,
                price=price,
                price_kg=price_kg
            )
            # Add the product to the list of products.
            products.append(product)
        except Exception as e:
            # Handle the error.
            print(f'Error scraping product: {e}')
            # Create a Product object with the `Not available` values.
            product = Product(
                title='Not available',
                price='Not available',
                price_kg='Not available'
            )
            # Add the product to the list of products.
            products.append(product)

    return products


    

# asyncio.run(scrape_mercadona())        
# asyncio.run(scrape_carrefour())   
# asyncio.run(scrape_dia())    
# asyncio.run(scrape_el_jamon())

