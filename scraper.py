import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
import asyncio
from config import *
from model import Product
import re
from typing import Optional
import json
import logging







async def scrape_url_el_jamon(client: httpx.AsyncClient, url: str, logger: logging.Logger) -> Product:
    """
    Scrape the given URL to retrieve product information from 'https://www.supermercadoseljamon.com'.
    Args:
        client (httpx.AsyncClient): An instance of httpx.AsyncClient used to make HTTP requests.
        url (str): The URL of the product page.
    Returns:
        product (Product): An instance of the Product class containing the scraped product information. If an error occurs during scraping, a Product instance with 'Not available' values will be returned.
    """
    async with client.stream("GET", url) as response:
        html = await response.aread()
    parser = HTMLParser(html)
    try:
        title = parser.css_first('h1.tituloProducto').text()
        
        price_rebajado = parser.css_first("#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-oferta > span")
        price_original = parser.css_first("#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-original > span")
        
        if price_rebajado:
            price = price_rebajado.text()
        else:
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
        logger.error(f'Error scraping product: {e}')
        # Create a Product object with the `Not available` values.
        product = Product(
            title='Not available',
            price='Not available',
            price_kg='Not available'
        )
    logger.info(product)               
    return product
        


async def scrape_url_dia(client: httpx.AsyncClient, url: str, logger: logging.Logger) -> Product:
    """
    Asynchronously scrapes the given URL.
    Args:
        client: The HTTP client to use for making requests.
        url: The URL to scrape.
    Returns:
        The scraped product information. If an error occurs during scraping, a Product object with the `Not available` values is returned.
    """
    
    response = await client.get(url)
    html = response.text
    parser = HTMLParser(html)
    try:
        title = parser.css_first('h1.product-title').text().strip()
        price = parser.css_first('p.buy-box__active-price').text().strip()
        price = re.findall(r'\d+,\d+', price)
        price_kg = parser.css_first('p.buy-box__price-per-unit').text().strip()
        price_kg = re.findall(r'\d+,\d+', price_kg)
        product = Product(
            title=title,
            price=price[0],
            price_kg=price_kg[0]
        )
    except Exception as e:
        logger.error(f'Error scraping product: {e}')
        product = Product(
            title='Not available',
            price='Not available',
            price_kg='Not available'
        )
    logger.info(product)

    return product


async def scrape_url_carrefour(client: httpx.AsyncClient, url: str, logger: logging.Logger) -> Product:
    """
    Scrapes the given URL to extract product information.
    Args:
        client (ClientSession): The aiohttp client session.
        url (str): The URL to scrape.
    Returns:
        Product: The scraped product information.
    """
    try:
        response = await client.get(url)
        html = response.text
        parser = HTMLParser(html)
        title = parser.css_first('h1.product-header__name').text().strip()
        price = parser.css_first('span.buybox__price').text().strip()
        price = re.findall(r'\d+,\d+', price)
        price_kg = parser.css_first('div.buybox__price-per-unit').text().strip()
        price_kg = re.findall(r'\d+,\d+', price_kg)
        product = Product(title=title, price=price[0], price_kg=price_kg[0])
    except Exception as e:
        logger.error(f'Error scraping product: {e}')
        product = Product(title='Not available', price='Not available', price_kg='Not available')
    logger.info(product)
    return product



async def scrape_url_mercadona(client: httpx.AsyncClient, url: str, logger: logging.Logger) -> Product:
    """
    Asynchronously scrapes the given URL and extracts product information.
    Args:
        client (httpx.AsyncClient): The httpx client session.
        url (str): The URL of the webpage to scrape.
    Returns:
        Product: A Product object containing the scraped product information.
    """
    
    try:
        async with client.stream("GET", url) as response:
            data = await response.aread()
            data = json.loads(data)
            title = data['display_name']
            price = data['price_instructions']['unit_price']
            price_kg = data['price_instructions']['bulk_price']
    except Exception as e:
        logger.error(f'Error scraping product: {e}')
        title = 'Not available'
        price = 'Not available'
        price_kg = 'Not available'

    product = Product(
        title=title,
        price=price,
        price_kg=price_kg
    )
    logger.info(product)
    return product


    



    


