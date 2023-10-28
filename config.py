
import pathlib

CERT = pathlib.Path('ISRG Root X2.crt')
HEADERS = {

    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',

}

HEADERS_MERCADONA = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60',
    }


EL_JAMON_URL = {

    'picos_integrales': 'https://www.supermercadoseljamon.com/detalle/-/Producto/picos-finos-integrales-250g/23025302',
    'aceitunas': 'https://www.supermercadoseljamon.com/detalle/-/Producto/aceituna-con-hueso-frasco-500g/13011253',
    'huevos': 'https://www.supermercadoseljamon.com/detalle/-/Producto/huevos-m-mediano-12ud/11099025',
    'pimientos': 'https://www.supermercadoseljamon.com/detalle/-/Producto/pimientos-finos-kg/54001161',
    'pizza-atún': 'https://www.supermercadoseljamon.com/detalle/-/Producto/pizza-atun-y-bacon-400g/11097605',
    'pechuga-pollo': 'https://www.supermercadoseljamon.com/detalle/-/Producto/pechuga-de-pollo-kg/93003100'

}

DIA_URL = {

    'picos_integrales': 'https://www.dia.es/panes-harinas-y-masas/picos-y-panes-tostados/p/59304?analytics_list_id=S0001&analytics_list_name=search&index=1',
    'aceitunas': 'https://www.dia.es/patatas-fritas-encurtidos-y-frutos-secos/aceitunas-y-encurtidos/p/46239?analytics_list_id=S0001&analytics_list_name=search&index=3',
    'huevos': 'https://www.dia.es/leche-huevos-y-mantequilla/huevos/p/274009?analytics_list_id=S0001&analytics_list_name=search&index=2',
    'pimientos': 'https://www.dia.es/verduras/tomates-pimientos-y-pepinos/p/116?analytics_list_id=S0001&analytics_list_name=search&index=1',
    'pizza-atún': 'https://www.dia.es/pizzas-y-platos-preparados/pizzas/p/30480?analytics_list_id=S0001&analytics_list_name=search&index=6',
    'pechuga-pollo':'https://www.dia.es/carniceria/pollo/p/261371?analytics_list_id=S0001&analytics_list_name=search&index=1'
}

CARREFOUR_URL = {

    'picos_integrales': 'https://www.carrefour.es/supermercado/colines-integrales-carrefour-250-g/R-prod970952/p',
    'aceitunas': 'https://www.carrefour.es/supermercado/aceitunas-verdes-manzanilla-sin-hueso-carrefour-400-g/R-VC4AECOMM-488058/p',
    'huevos': 'https://www.carrefour.es/supermercado/huevos-frescos-carrefour-el-mercado-24-ud/R-VC4AECOMM-307898/p',
    'pimientos': 'https://www.carrefour.es/supermercado/pimiento-verde-italiano-1-kg-aprox/R-536001616/p',
    'pizza-atún': 'https://www.carrefour.es/supermercado/pizza-bolonesa-carrefour-375-g/R-530363194/p',
    'pechuga-pollo':'https://www.carrefour.es/supermercado/pechuga-de-pollo-carrefour-12-kg-aprox/R-644001825/p',

}

MERCADONA_URL = {

    'picos_integrales': 'https://tienda.mercadona.es/api/products/86215/',
    'aceitunas': 'https://tienda.mercadona.es/api/products/80016/?lang=es&wh=svq1',
    'huevos': 'https://tienda.mercadona.es/api/products/31002/?lang=es&wh=svq1',
    'pimientos': 'https://tienda.mercadona.es/api/products/69443/?lang=es&wh=svq1',
    'pizza-atún': 'https://tienda.mercadona.es/api/products/63582/?lang=es&wh=svq1',
    'pechuga-pollo':'https://tienda.mercadona.es/api/products/3682/?lang=es&wh=svq1',
    

}