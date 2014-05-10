# -*- coding: utf-8 -*-
from django.db import models

import unicodedata


def normalize(s):
    """
        >>> normalize(u'Ñonos útiles')
        'nonos utiles'
    """
    try:
        normal = unicodedata.normalize('NFKD', cadena)
    except TypeError:
        cadena = cadena.decode('iso-8859-1')
        normal = unicodedata.normalize('NFKD', cadena)
    return normal.encode('ASCII', 'ignore').lower()



# Create your models here.

class Newspaper(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()


class Article(models.Model):

    date = models.DateField()
    title = models.CharField(max_length=300)
    url = models.URLField()

    lead = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    epigraph = models.TextField(null=True, blank=True)
    image_url = models.URLField(max_length=200, null=True, blank=True)
    image_epigraph = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)

