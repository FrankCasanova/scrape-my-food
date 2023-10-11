from typing import List, Dict
from fastapi import FastAPI, HTTPException
from model import *
from scraper import *
import asyncio

app = FastAPI()

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
    try:
        list_products = [await scrape_url_mercadona(MERCADONA_URL[url]) for url in MERCADONA_URL]
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
    try:
        list_products = [await scrape_url_carrefour(CARREFOUR_URL[url]) for url in CARREFOUR_URL]
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
    try:
        list_products = [await scrape_url_el_jamon(EL_JAMON_URL[url]) for url in EL_JAMON_URL]
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
    try:
        list_products = [await scrape_url_dia(DIA_URL[url]) for url in DIA_URL]  
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
    try:
        list_products = []
        for url in MERCADONA_URL:
            list_products.append(await scrape_url_mercadona(MERCADONA_URL[url]))
        for url in CARREFOUR_URL:
            list_products.append(await scrape_url_carrefour(CARREFOUR_URL[url]))
        for url in EL_JAMON_URL:
            list_products.append(await scrape_url_el_jamon(EL_JAMON_URL[url]))
        for url in DIA_URL:
            list_products.append(await scrape_url_dia(DIA_URL[url]))
        
        return list_products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#quiero un endpoint que devuelva el el titulo, precio y precio por kilo de los "picos_integrales" de todos los supermercados
@app.get("/picos-integrales", response_model=List[Product])
async def get_picos_integrales():
    """
    Returns a list of `Product` models containing the title, price, and price per kilo
    of the "picos_integrales" from all supermarkets.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    try:
        list_products = [
            await scrape_url_mercadona(MERCADONA_URL['picos_integrales']),
            await scrape_url_carrefour(CARREFOUR_URL['picos_integrales']),
            await scrape_url_el_jamon(EL_JAMON_URL['picos_integrales']),
            await scrape_url_dia(DIA_URL['picos_integrales'])
        ]
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
    try:
        list_products = [
            await scrape_url_mercadona(MERCADONA_URL['aceitunas']),
            await scrape_url_carrefour(CARREFOUR_URL['aceitunas']),
            await scrape_url_el_jamon(EL_JAMON_URL['aceitunas']),
            await scrape_url_dia(DIA_URL['aceitunas'])
        ]
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
    try:
        list_products = [
            await scrape_url_mercadona(MERCADONA_URL['pimientos']),
            await scrape_url_carrefour(CARREFOUR_URL['pimientos']),
            await scrape_url_el_jamon(EL_JAMON_URL['pimientos']),
            await scrape_url_dia(DIA_URL['pimientos'])
        ]
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
    try:
        list_products = [
            await scrape_url_mercadona(MERCADONA_URL['huevos']),
            await scrape_url_carrefour(CARREFOUR_URL['huevos']),
            await scrape_url_el_jamon(EL_JAMON_URL['huevos']),
            await scrape_url_dia(DIA_URL['huevos'])
        ]
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
    try:
        list_products = [
            await scrape_url_mercadona(MERCADONA_URL['pizza-atún']),
            await scrape_url_carrefour(CARREFOUR_URL['pizza-atún']),
            await scrape_url_el_jamon(EL_JAMON_URL['pizza-atún']),
            await scrape_url_dia(DIA_URL['pizza-atún'])
        ]
        return list_products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.2", port=8000, reload=True)
