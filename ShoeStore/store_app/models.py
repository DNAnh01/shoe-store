from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Filter_Price(models.Model):
    FILTER_PRICE = (
        ('1 TO 10', '1 TO 10'),
        ('10 TO 20', '10 TO 20'),
        ('20 TO 30', '20 TO 30'),
        ('30 TO 40', '30 TO 40'),
        ('40 TO 50', '40 TO 50'),
        ('50 TO 60', '50 TO 60'),
        ('60 TO 70', '60 TO 70'),
        ('70 TO 80', '70 TO 80'),
        ('80 TO 90', '80 TO 90'),
        ('90 TO 100', '90 TO 100')
    )
    price = models.CharField(choices=FILTER_PRICE, max_length=60)
    def __str__(self):
        return self.price

class Product(models.Model):
    CONDITION = (('New', 'New'), ('Old', 'Old'))
    STOCK = (('IN STOCK', 'IN STOCK'), ('OUT OF STOCK', 'OUT OF STOCK'))
    STATUS = (('Publish', 'Publish'), ('Draft', 'Draft'))

    unique_id = models.CharField(unique=True, max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='Product_images/img')
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    condition = models.CharField(choices=CONDITION, max_length=100)
    information = RichTextField(null=True)
    description = RichTextField(null=True)
    stock = models.CharField(choices=STOCK, max_length=200)
    status = models.CharField(choices=STATUS, max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    # relation
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Filter_Price, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.unique_id is None and self.created_date and self.id:
            self.unique_id = self.created_date.strftime('75%Y%M%D23') + str(self.id)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Images(models.Model):
    image = models.ImageField(upload_to='Product_images/img')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Contact_us(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email