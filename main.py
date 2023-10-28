from typing import List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import *
from scraper import *
import asyncio
import httpx
from config import *
import logging
import time

# origins = [
#     "http://127.0.0.1:5500",  # Asegúrate de cambiar esto a tus propios orígenes
# ]



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],	
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

@app.get("/mercadona",
    status_code=200,
    response_model=List[Product],
    response_model_exclude_unset=True,summary="Mercadona",
    description="Returns a list of `Product` models scraped from the Mercadona website.",)
async def get_mercadona_products():
    """
    Returns a list of `Product` models scraped from the Mercadona website.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS_MERCADONA) as client:
        try:
            list_products = [await scrape_url_mercadona(client=client, url=MERCADONA_URL[url], logger=logger) for url in MERCADONA_URL]
            end_time = time.time()
            logger.info(f'Time to scrape Mercadona: {end_time - start_time}')
            return list_products
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/carrefour",
         status_code=200,
         response_model=List[Product],
         response_model_exclude_unset=True,summary="Carrefour",
         description="Returns a list of `Product` models scraped from the Carrefour website.",
         )
async def get_carrefour_products():
    """
    Returns a list of `Product` models scraped from the Carrefour website.
    Parameters:
        None
    Returns:
        List[Product]: A list of `Product` models.
    Raises:
        HTTPException: If an exception occurs during the scraping process.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        try:
            list_products = [await scrape_url_carrefour(client=client, url=CARREFOUR_URL[url], logger=logger) for url in CARREFOUR_URL]
            end_time = time.time()
            logger.info(f'Time to scrape Carrefour: {end_time - start_time}')
            return list_products

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/el-jamon",
        response_model=List[Product],
        response_model_exclude_unset=True,summary="El Jamón",
        description="Returns a list of `Product` models scraped from the El Jamón website.",)
async def get_el_jamon_products():
    """
    Returns a list of `Product` models scraped from the El Jamón website.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS,verify=False) as client:
        await client.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
        await client.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
        try:
            list_products = [await scrape_url_el_jamon(client=client, url=EL_JAMON_URL[url], logger=logger) for url in EL_JAMON_URL]
            end_time = time.time()
            logger.info(f'Time to scrape El Jamón: {end_time - start_time}')
            return list_products
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/dia", response_model=List[Product])
async def get_dia_products():
    """
    Returns a list of `Product` models scraped from the Día website.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        try:
            list_products = [await scrape_url_dia(client=client, url=DIA_URL[url], logger=logger) for url in DIA_URL] 
            end_time = time.time() 
            logger.info(f'Time to scrape Día: {end_time - start_time}')
            return list_products
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/prices",
         status_code=200,
         response_model_exclude_unset=True,summary="Prices",
         description="Returns a list of lists of `Product` models scraped from different stores.")
async def get_prices():
    """
    Returns a list of lists of `Product` models scraped from different stores.
    Raises:
        HTTPException: If the scraping process fails
    Returns:
        List[List[Product]]: A list of lists of `Product` models.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        client_EL_JAMON = httpx.AsyncClient(headers=HEADERS,verify=False)
        await client_EL_JAMON.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
        await client_EL_JAMON.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
        try:
            list_products = []
            for url in MERCADONA_URL:
                client.headers.update(HEADERS_MERCADONA)
                list_products.append(await scrape_url_mercadona(client=client, url=MERCADONA_URL[url], logger=logger))
            for url in CARREFOUR_URL:
                client.headers.update(HEADERS)
                list_products.append(await scrape_url_carrefour(client=client, url=CARREFOUR_URL[url], logger=logger))
            for url in EL_JAMON_URL:
                list_products.append(await scrape_url_el_jamon(client=client_EL_JAMON, url=EL_JAMON_URL[url], logger=logger))
            for url in DIA_URL:
                list_products.append(await scrape_url_dia(client=client, url=DIA_URL[url], logger=logger))
                
            await client_EL_JAMON.aclose()
            end_time = time.time()
            logger.info(f'Time to scrape Mercadona: {end_time - start_time}')
            return list_products
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

#quiero un endpoint que devuelva el el titulo, precio y precio por kilo de los "picos_integrales" de todos los supermercados
from typing import List

@app.get("/picos-integrales", response_model=List[Product])
async def get_picos_integrales() -> List[Product]:
    """
    Retrieves a list of products for 'picos-integrales' from various supermarkets.
    
    Returns:
        List[Product]: A list of products for 'picos-integrales' from different supermarkets.
        
    Raises:
        HTTPException: If there is an error while retrieving the products.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        async with httpx.AsyncClient(headers=HEADERS, verify=False) as client_el_jamon:
            await client_el_jamon.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
            await client_el_jamon.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')

            try:
                list_products: List[Product] = []
                client.headers.update(HEADERS_MERCADONA)
                list_products.append(await scrape_url_mercadona(client=client, url=MERCADONA_URL['picos_integrales'], logger=logger))
                client.headers.update(HEADERS)
                list_products.append(await scrape_url_carrefour(client=client, url=CARREFOUR_URL['picos_integrales'], logger=logger))
                list_products.append(await scrape_url_el_jamon(client=client_el_jamon, url=EL_JAMON_URL['picos_integrales'], logger=logger))
                list_products.append(await scrape_url_dia(client=client, url=DIA_URL['picos_integrales'], logger=logger))
                end_time = time.time()
                return list_products
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

@app.get('/aceitunas', response_model=List[Product])
async def get_aceitunas():
    """
    Returns a list of `Product` models containing the title, price, and price per kilo
    of the "aceitunas" from all supermarkets.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        async with httpx.AsyncClient(headers=HEADERS, verify=False) as client_el_jamon:
            await client_el_jamon.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
            await client_el_jamon.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
            try:
                list_products: List[Product] = []
                client.headers.update(HEADERS_MERCADONA)
                list_products.append(await scrape_url_mercadona(client=client, url=MERCADONA_URL['aceitunas'], logger=logger))
                client.headers.update(HEADERS)
                list_products.append(await scrape_url_carrefour(client=client, url=CARREFOUR_URL['aceitunas'], logger=logger))
                list_products.append(await scrape_url_el_jamon(client=client_el_jamon, url=EL_JAMON_URL['aceitunas'], logger=logger))
                list_products.append(await scrape_url_dia(client=client, url=DIA_URL['aceitunas'], logger=logger))
                end_time = time.time()
                logger.info(f'Time to scrape Mercadona: {end_time - start_time}')
                return list_products
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

@app.get('/pimientos', response_model=List[Product])
async def get_pimientos():
    """
    Returns a list of `Product` models containing the title, price, and price per kilo
    of the "pimientos" from all supermarkets.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        async with httpx.AsyncClient(headers=HEADERS, verify=False) as client_el_jamon:
            await client_el_jamon.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
            await client_el_jamon.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
            try:
                list_products: List[Product] = []
                client.headers.update(HEADERS_MERCADONA)
                list_products.append(await scrape_url_mercadona(client=client, url=MERCADONA_URL['pimientos'], logger=logger))
                client.headers.update(HEADERS)
                list_products.append(await scrape_url_carrefour(client=client, url=CARREFOUR_URL['pimientos'], logger=logger))
                list_products.append(await scrape_url_el_jamon(client=client_el_jamon, url=EL_JAMON_URL['pimientos'], logger=logger))
                list_products.append(await scrape_url_dia(client=client, url=DIA_URL['pimientos'], logger=logger))
                end_time = time.time()
                logger.info(f'Time to scrape pimientos: {end_time - start_time}')
                return list_products
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

@app.get('/huevos', response_model=List[Product])
async def get_huevos():
    """
    Returns a list of `Product` models containing the title, price, and price per kilo
    of the "huevos" from all supermarkets.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        async with httpx.AsyncClient(headers=HEADERS, verify=False) as client_el_jamon:
            await client_el_jamon.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
            await client_el_jamon.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
            try:
                list_products: List[Product] = []
                client.headers.update(HEADERS_MERCADONA)
                list_products.append(await scrape_url_mercadona(client=client, url=MERCADONA_URL['huevos'], logger=logger))
                client.headers.update(HEADERS)
                list_products.append(await scrape_url_carrefour(client=client, url=CARREFOUR_URL['huevos'], logger=logger))
                list_products.append(await scrape_url_el_jamon(client=client_el_jamon, url=EL_JAMON_URL['huevos'], logger=logger))
                list_products.append(await scrape_url_dia(client=client, url=DIA_URL['huevos'], logger=logger))
                end_time = time.time()
                logger.info(f'Time to scrape Huevos: {end_time - start_time}')
                return list_products
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

@app.get('/pizza-atún', response_model=List[Product])
async def get_pizza_atun():
    """
    Returns a list of `Product` models containing the title, price, and price per kilo
    of the "pizza-atún" from all supermarkets.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        async with httpx.AsyncClient(headers=HEADERS, verify=False) as client_el_jamon:
            await client_el_jamon.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
            await client_el_jamon.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
            try:
                list_products: List[Product] = []
                client.headers.update(HEADERS_MERCADONA)
                list_products.append(await scrape_url_mercadona(client=client, url=MERCADONA_URL['pizza-atún'], logger=logger))
                client.headers.update(HEADERS)
                list_products.append(await scrape_url_carrefour(client=client, url=CARREFOUR_URL['pizza-atún'], logger=logger))
                list_products.append(await scrape_url_el_jamon(client=client_el_jamon, url=EL_JAMON_URL['pizza-atún'], logger=logger))
                list_products.append(await scrape_url_dia(client=client, url=DIA_URL['pizza-atún'], logger=logger))
                end_time = time.time()
                logger.info(f'Time to scrape pizza-atún: {end_time - start_time}')
                return list_products
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


    
@app.get('/pechuga-pollo', response_model=List[Product])
async def get_pechuga_pollo():
    """
    Returns a list of `Product` models containing the title, price, and price per kilo
    of the "pechuga-pollo" from all supermarkets.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    start_time = time.time()
    async with httpx.AsyncClient(headers=HEADERS) as client:
        async with httpx.AsyncClient(headers=HEADERS, verify=False) as client_el_jamon:
            await client_el_jamon.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
            await client_el_jamon.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
            try:
                list_products: List[Product] = []
                client.headers.update(HEADERS_MERCADONA)
                list_products.append(await scrape_url_mercadona(client=client, url=MERCADONA_URL['pechuga-pollo'], logger=logger))
                client.headers.update(HEADERS)
                list_products.append(await scrape_url_carrefour(client=client, url=CARREFOUR_URL['pechuga-pollo'], logger=logger))
                list_products.append(await scrape_url_el_jamon(client=client_el_jamon, url=EL_JAMON_URL['pechuga-pollo'], logger=logger))
                list_products.append(await scrape_url_dia(client=client, url=DIA_URL['pechuga-pollo'], logger=logger))
                end_time = time.time()
                logger.info(f'Time to scrape pechuga-pollo: {end_time - start_time}')
                return list_products
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))