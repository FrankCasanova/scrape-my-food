import httpx
from selectolax.parser import HTMLParser
import asyncio

async def main():
    async with httpx.AsyncClient(verify=False) as client:
        
        await client.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
        await client.get('https://www.supermercadoseljamon.com/delegate/seleccionarCodPostalAjaxServletFood?accion=enviarCodPostal&cp=21004&locale=es')
        response = await client.get('https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302')
        
        html = response.text
        
        parse = HTMLParser(html)
        
        price = parse.css_first('#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-oferta > span').text()
        
        print(price)
        

asyncio.run(main())

