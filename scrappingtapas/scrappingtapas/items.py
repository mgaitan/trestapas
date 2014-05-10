# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

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
