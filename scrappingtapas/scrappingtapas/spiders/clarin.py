from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.item import Item, Field
from scrapy.http.request import Request

import datetime as dt
import urlparse
import urllib2, urllib
import re
import sys

URL_TAPA = """http://www.clarin.com/edicion-impresa.html?fecha="""

NUM_DIAS = 180

class ArticuloItem(Item):
    fecha = Field()
    antetitulo = Field()
    titulo = Field()
    bajada = Field()
    texto = Field()
    imagen = Field()
    url_articulo = Field()
    url_imagen = Field()
    autor = Field()


FIELD_XPATHS = {
    'antetitulo': './h4/text()',
    'titulo': './h2/a/text()',
    'url_articulo': './h2/a/@href',
    # 'bajada': ''
    # 'texto': ''
    # 'imagen': ''
    # 'url_imagen': ''
    # 'autor': ''
}

def extraer_fecha(url):
    year, month, day = (int(p) for p in (url[-8:-4], url[-4:-2], url[-2:]))
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


class TitularesClarinSpider(CrawlSpider):
    name = 'clarin'
    allowed_domains = ['clarin.com']
    undia = dt.timedelta(days=1)
    hoy = dt.date.today()
    fechas = [hoy - i*undia for i in range(NUM_DIAS)]
    fechas = [fecha.strftime("%Y%m%d") for fecha in fechas]
    start_urls = [URL_TAPA + fecha for fecha in fechas]

    def parse_start_url(self, response):
        yield Request(response.url,
                      meta=response.meta,
                      callback=self.parse_page,
                      dont_filter=True)

    def parse_page(self, response):
        # sys.stderr.write("parsing page %d for day %d\n" % (page, day))
        parsed_url = urlparse.urlparse(response.url)
        sel = Selector(response)

        xpathtitular = '//*[contains(@class,"tapa")]//li'
        nodos_titulares = sel.xpath(xpathtitular)

        for nodo in nodos_titulares:
            articulo = ArticuloItem()
            for field, xpath in FIELD_XPATHS.items():
                articulo[field] = extract_if_present(nodo, xpath)

            articulo['url_articulo'] = "http://www.clarin.com/" + articulo['url_articulo']
            articulo['fecha'] = extraer_fecha(response.url)
            yield articulo

if __name__ == '__main__':
    spider = TitularesClarinSpider()
