from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Products)
admin.site.register(models.Cart)
admin.site.register(models.order)
admin.site.register(models.OrderItem)
admin.site.register(models.Category)