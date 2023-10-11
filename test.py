import httpx
from selectolax.parser import HTMLParser
import asyncio
from config import *
import httpx
from model import Product
import re

async def scrape_url_dia(url):
    async with httpx.AsyncClient(headers=HEADERS,verify=False) as client:
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
               
    
    return print(product)


asyncio.run(scrape_url_dia(DIA_URL['picos_integrales']))