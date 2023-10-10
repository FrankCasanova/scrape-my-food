import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302")
        await page.click("#button")
        await page.fill("#seleccionarCp", "21004")
        await page.click("#aceptarPorCp")
        price = await page.inner_text("#_DetalleProductoFoodPortlet_WAR_comerzziaportletsfood_frmDatos > div.wrapp-detalle-precio > div.wrap-dp.dp-oferta > span")
        print(price)
        await browser.close()

asyncio.run(main())
