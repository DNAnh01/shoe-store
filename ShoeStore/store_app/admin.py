from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Filter_Price)