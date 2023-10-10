import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
from playwright.async_api import async_playwright
import asyncio


HEADERS = {

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',

}


EL_JAMON_URL = {

    'picos_integrales': 'https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302',
    'aceitunas': 'https://www.supermercadoseljamon.com/detalle/-/Producto/aceituna-con-hueso-frasco-500g/13011253',
    'huevos': 'https://www.supermercadoseljamon.com/detalle/-/Producto/huevos-m-mediano-12ud/11099025',
    'pimientos': 'https://www.supermercadoseljamon.com/detalle/-/Producto/pimientos-finos-kg/54001161',
    'pizza-atún': 'https://www.supermercadoseljamon.com/detalle/-/Producto/pizza-atun-y-bacon-400g/11097605'

}

DIA_URL = {

    'picos_integrales': 'https://www.dia.es/panes-harinas-y-masas/picos-y-panes-tostados/p/59304?analytics_list_id=S0001&analytics_list_name=search&index=1',
    'aceitunas': 'https://www.dia.es/panes-harinas-y-masas/picos-y-panes-tostados/p/59304?analytics_list_id=S0001&analytics_list_name=search&index=1',
    'huevos': 'https://www.dia.es/leche-huevos-y-mantequilla/huevos/p/274009?analytics_list_id=S0001&analytics_list_name=search&index=2',
    'pimientos': 'https://www.dia.es/verduras/tomates-pimientos-y-pepinos/p/116?analytics_list_id=S0001&analytics_list_name=search&index=1',
    'pizza-atún': 'https://www.dia.es/pizzas-y-platos-preparados/pizzas/p/30480?analytics_list_id=S0001&analytics_list_name=search&index=6'

}

CARREFOUR_URL = {

    'picos_integrales': 'https://www.carrefour.es/supermercado/colines-integrales-carrefour-250-g/R-prod970952/p',
    'aceitunas': 'https://www.carrefour.es/supermercado/aceitunas-verdes-manzanilla-sin-hueso-carrefour-400-g/R-VC4AECOMM-488058/p',
    'huevos': 'https://www.carrefour.es/supermercado/huevos-frescos-carrefour-el-mercado-24-ud/R-VC4AECOMM-307898/p',
    'pimientos': 'https://www.carrefour.es/supermercado/pimiento-verde-italiano-1-kg-aprox/R-536001616/p',
    'pizza-atún': 'https://www.carrefour.es/supermercado/pizza-de-atun-carrefour-350-g/R-prod590834/p'

}

MERCADONA_URL = {

    'picos_integrales': 'https://tienda.mercadona.es/api/products/86215/',
    'aceitunas': 'https://tienda.mercadona.es/api/products/80016/?lang=es&wh=svq1',
    'huevos': 'https://tienda.mercadona.es/api/products/31002/?lang=es&wh=svq1',
    'pimientos': 'https://tienda.mercadona.es/api/products/69443/?lang=es&wh=svq1',
    'pizza-atún': 'https://tienda.mercadona.es/api/products/63582/?lang=es&wh=svq1'

}






async def scrape_el_jamon():

    async with async_playwright() as p:

        browser = await p.chromium.launch()
        context = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60')
        screen = await context.new_page()
        products = []
        for key in EL_JAMON_URL:
            await screen.goto(EL_JAMON_URL[key])
            button = screen.get_by_role("button", name="Ver precio")
            button_count = await button.count()
            if button_count > 0:
                await screen.get_by_role("button", name="Ver precio").click()
                await screen.locator("#seleccionarCp").click()
                await screen.locator("#seleccionarCp").fill("21004")
                await screen.get_by_role("button", name="Aceptar").click()
                await screen.wait_for_timeout(1000)
                await screen.goto(EL_JAMON_URL[key])
                title = await screen.query_selector('h1.tituloProducto')
                price = await screen.query_selector('span.d-importe')
                price_kg = await screen.query_selector('div.texto-porKilo')
                title = await title.inner_text()
                price = await price.inner_text()
                price_kg = await price_kg.inner_text()
                el_jamon = {

                    'title': title,
                    'price': price,
                    'price_kg': price_kg,

                }

                products.append(el_jamon)
            title = await screen.query_selector('h1.tituloProducto')
            price = await screen.query_selector('span.d-importe')
            price_kg = await screen.query_selector('div.texto-porKilo')
            title = await title.inner_text()
            price = await price.inner_text()
            price_kg = await price_kg.inner_text()
            el_jamon = {

                'title': title,
                'price': price,
                'price_kg': price_kg,

            }

            products.append(el_jamon)
            
        return print(products)
        await browser.close()

async def scrape_dia():
    
    products = []
    for key in DIA_URL:
        response =  httpx.get(DIA_URL[key], headers=HEADERS)
        html = response.content.decode('utf-8')
        parser = HTMLParser(html)
        title = parser.css_first('h1.product-title').text().strip()
        price = parser.css_first('p.buy-box__active-price').text().strip()
        price_kg = parser.css_first('p.buy-box__price-per-unit').text().strip()
        
        dicts = {
            'title': title,
            'price': price,
            'pricec_kg': price_kg
        }
        
        products.append(dicts)
    
    return print(products)


async def scrape_carrefour():
    
    products = []
    for key in CARREFOUR_URL:
        response =  httpx.get(CARREFOUR_URL[key], headers=HEADERS)
        html = response.content.decode('utf-8')
        parser = HTMLParser(html)
        title = parser.css_first('h1.product-header__name').text().strip()
        price = parser.css_first('span.buybox__price').text().strip()
        price_kg = parser.css_first('div.buybox__price-per-unit').text().strip()
        
        dicts = {
            'title': title,
            'price': price,
            'pricec_kg': price_kg
        }
        
        products.append(dicts)
    
    return print(products)

async def scrape_mercadona():
    
    HEADERS = {

    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',

    }
    
    products = []
    for key in MERCADONA_URL:
        response =  httpx.get(MERCADONA_URL[key], headers=HEADERS)
        data = response.json()
        title =  data['display_name']
        price = data['price_instructions']['unit_price'] + ' eur'
        price_kg = data['price_instructions']['bulk_price'] + ' eur'
    
        dicts = {
            'title' : title,
            'precio' : price,
            'price_kg' : price_kg
        }
        
        products.append(dicts)
    
    return print(products)

asyncio.run(scrape_mercadona())        
asyncio.run(scrape_carrefour())   
asyncio.run(scrape_dia())    
asyncio.run(scrape_el_jamon())

