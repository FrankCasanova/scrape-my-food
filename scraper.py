import httpx
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
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
    'aceitunas': 'https://www.dia.es/patatas-fritas-encurtidos-y-frutos-secos/aceitunas-y-encurtidos/p/46239?analytics_list_id=S0001&analytics_list_name=search&index=3',
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

@dataclass
class Product:
    title: str
    price: str
    price_kg: str




async def scrape_el_jamon():

    async with httpx.AsyncClient(headers=HEADERS, verify=False) as client:
        
        await client.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
        await client.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
        
        products = []
        for key in EL_JAMON_URL:
            response =  await client.get(EL_JAMON_URL[key])
        
            html = response.text
            
            parse = HTMLParser(html)
            
            title = parse.css_first('h1.tituloProducto').text()
            price_rebajado = parse.css_first("#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-oferta > span")
            if price_rebajado:
                price = price_rebajado.text()
            else:
                price_original = parse.css_first("#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-original > span")
                price = price_original.text()
                
            price_kg = parse.css_first('div.texto-porKilo').text()
        
            product = Product(title,price,price)
            products.append(product)
            
        for product in products:
            print(asdict(product))        
        return products
        

async def scrape_dia():
    
    products = []
    for key in DIA_URL:
        response =  httpx.get(DIA_URL[key], headers=HEADERS)
        html = response.content.decode('utf-8')
        parser = HTMLParser(html)
        title = parser.css_first('h1.product-title').text().strip()
        price = parser.css_first('p.buy-box__active-price').text().strip()
        price_kg = parser.css_first('p.buy-box__price-per-unit').text().strip()
        
        product = Product(title,price,price)
        products.append(product)
            
    for product in products:
        print(asdict(product))        
    return products


async def scrape_carrefour():
    
    products = []
    for key in CARREFOUR_URL:
        response =  httpx.get(CARREFOUR_URL[key], headers=HEADERS)
        html = response.content.decode('utf-8')
        parser = HTMLParser(html)
        title = parser.css_first('h1.product-header__name').text().strip()
        price = parser.css_first('span.buybox__price').text().strip()
        price_kg = parser.css_first('div.buybox__price-per-unit').text().strip()
        
        product = Product(title,price,price)
        products.append(product)
        
    for product in products:
        print(asdict(product))        
    return products

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
    
        product = Product(title,price,price)
        products.append(product)
        
    for product in products:
        print(asdict(product))        
    return products

asyncio.run(scrape_mercadona())        
asyncio.run(scrape_carrefour())   
asyncio.run(scrape_dia())    
asyncio.run(scrape_el_jamon())

