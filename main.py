from typing import List, Dict
from fastapi import FastAPI, HTTPException
from model import *
from scraper import *
import asyncio

app = FastAPI()

@app.get("/mercadona", response_model=List[Product])
async def get_mercadona_products():
    """
    Returns a list of `Product` models scraped from the Mercadona website.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    try:
        products = await scrape_mercadona()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/carrefour", response_model=List[Product])
async def get_carrefour_products():
    """
    Returns a list of `Product` models scraped from the Carrefour website.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    try:
        products = await scrape_carrefour()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/el-jamon", response_model=List[Product])
async def get_el_jamon_products():
    """
    Returns a list of `Product` models scraped from the El Jamón website.
    Raises:
        HTTPException: If the scraping process fails.
    Returns:
        List[Product]: A list of `Product` models.
    """
    try:
        products = await scrape_el_jamon()
        return products
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
        products = await scrape_dia()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/prices", response_model=List[List[Product]])
async def get_prices():
    """
    Returns a list of lists of `Product` models scraped from different stores.
    Raises:
        HTTPException: If the scraping process fails
    Returns:
        List[List[Product]]: A list of lists of `Product` models.
    """
    try:
        products = [
            await scrape_dia(),
            await scrape_el_jamon(),
            await scrape_carrefour(),
            await scrape_mercadona(),     
        ]
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.2", port=8000)
