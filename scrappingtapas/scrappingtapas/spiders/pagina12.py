from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item, Field
from scrapy.http.request import Request

from scrappingtapas.items import ArticuloItem

import datetime as dt
import urlparse
import urllib2, urllib
import re
import sys

class ArticuloItem(Item):
    url_articulo = Field()
    antetitulo = Field()
    fecha = Field()
    texto = Field()
    autor = Field()
    bajada = Field()
    titulo = Field()
    url_imagen = Field()
    orden = Field()


#  ejemplo: http://www.pagina12.com.ar/diario/principal/diario/index-2014-05-08.html
URL_TAPA = """http://www.pagina12.com.ar/diario/principal/diario/index-%s.html"""

NUM_DIAS = 180

FIELD_XPATHS = {
    'antetitulo': './/*[@class="volanta"]/text()',
    'titulo': './/a[@class="cprincipal"]/text()',
    'url_articulo': './/a[@class="cprincipal"]/@href',
    'autor': './/*[@class="autor"]/text()',
    'bajada': './/p[position()=last()]/text()',
    'url_imagen': '//img[@class="foto_titular"]/@src',
    # 'texto': ''
}

def extraer_fecha(url):
    fecha = url.split(".")[-2][-10:]
    year, month, day = (int(p) for p in fecha.split("-"))
    return dt.date(year, month, day)

def extract_if_present(node, xpath):
    '''
        Extracts the first child of node
        matching xpath.
        If none found, it returns "_"
    '''
    res = node.xpath(xpath).extract()
    if res:
        return res[0]
    else:
        return "_"


class TitularesPaginaSpider(CrawlSpider):
    name = 'pagina12'
    # allowed_domains = ['www.pagina12.com.ar']
    undia = dt.timedelta(days=1)
    hoy = dt.date.today()
    fechas = [hoy - i*undia for i in range(NUM_DIAS)]
    fechas = [fecha.strftime("%Y-%m-%d") for fecha in fechas]
    start_urls = [URL_TAPA % fecha for fecha in fechas]

    def parse_start_url(self, response):
        yield Request(response.url,
                      meta=response.meta,
                      callback=self.parse_page,
                      dont_filter=True)

    def parse_page(self, response):
        # sys.stderr.write("parsing page %d for day %d\n" % (page, day))
        parsed_url = urlparse.urlparse(response.url)
        sel = Selector(response)

        xpathtitular = '//*[@class="tapa_titulares"]/*[contains(@class,"noticia")]'
        nodos_titulares = sel.xpath(xpathtitular)

        for i, nodo in enumerate(nodos_titulares):
            articulo = ArticuloItem()
            for field, xpath in FIELD_XPATHS.items():
                articulo[field] = extract_if_present(nodo, xpath)

            articulo['fecha'] = extraer_fecha(response.url)
            articulo['antetitulo'] = articulo['antetitulo'][3:]
            articulo['url_articulo'] = 'http://www.pagina12.com.ar' + articulo['url_articulo']
            articulo['autor'] = articulo['autor'][4:]
            articulo['orden'] = i + 1
            yield articulo

if __name__ == '__main__':
    spider = TitularesClarinSpider()
