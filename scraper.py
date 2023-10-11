import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import asyncio
from config import *
from model import Product
import re




async def scrape_url_el_jamon(url):
    """
    Scrape the given URL to retrieve product information from 'https://www.supermercadoseljamon.com'.
    Args:
        url (str): The URL of the product page.
    Returns:
        products (Product): An instance of the Product class containing the scraped product information. If an error occurs during scraping, a Product instance with 'Not available' values will be returned.
    """
    async with httpx.AsyncClient(headers=HEADERS,verify=False) as client:
        await client.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
        await client.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
        response = await client.get(url)  
        html = response.text
        parser = HTMLParser(html)
        try:
            title = parser.css_first('h1.tituloProducto').text()
            price_rebajado = parser.css_first("#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-oferta > span")
            if price_rebajado:
                price = price_rebajado.text()
                price = re.findall(r'\d+,\d+', price)       
            else:
                price_original = parser.css_first("#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-original > span")
                price = price_original.text()
                price = re.findall(r'\d+,\d+', price)    
            price_kg = parser.css_first('div.texto-porKilo').text()
            price_kg = re.findall(r'\d+,\d+', price_kg)
                
            product = Product(
            title=title,
            price=price[0],
            price_kg=price_kg[0]
            )
            
            
        except Exception as e:
            # Handle the error.
            print(f'Error scraping product: {e}')
            # Create a Product object with the `Not available` values.
            product = Product(
                title='Not available',
                price='Not available',
                price_kg='Not available'
            )
                   
    return product
        

async def scrape_url_dia(url):
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(url)  
        html = response.text
        parser = HTMLParser(html)
        try:
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
        except Exception as e:
            # Handle the error.
            print(f'Error scraping product: {e}')
            # Create a Product object with the `Not available` values.
            product = Product(
                title='Not available',
                price='Not available',
                price_kg='Not available'
            )

    return product


async def scrape_url_carrefour(url):
    async with httpx.AsyncClient(verify=False, headers=HEADERS) as client:
        response = await client.get(url)
        html = response.text
        parser = HTMLParser(html)
        try:
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
    
    print(product)
              
    return product

async def scrape_url_mercadona(url):
    """
    Asynchronously scrapes the given URL and extracts product information.
    Args:
        url (str): The URL of the webpage to scrape.
    Returns:
        products: A list of Product objects containing the scraped product information.
    """
    HEADERS = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',
    }
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(url)
        html = response.text
        parser = HTMLParser(html)
        try:
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
    
        except Exception as e:
            # Handle the error.
            print(f'Error scraping product: {e}')
            # Create a Product object with the `Not available` values.
            product = Product(
                title='Not available',
                price='Not available',
                price_kg='Not available'
            )

    return product


    



    


