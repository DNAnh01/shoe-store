from django.db import models

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=200)

class Brand(models.Model):
    name = models.CharField(max_length=200)

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('1000 TO 10000', '1000 TO 10000'),
        ('10000 TO 20000', '10000 TO 20000'),
        ('20000 TO 30000', '20000 TO 30000'),
        ('30000 TO 40000', '30000 TO 40000'),
        ('40000 TO 50000', '40000 TO 50000')
    )
    price = models.CharField(choices=FILTER_PRICE, max_length=60)