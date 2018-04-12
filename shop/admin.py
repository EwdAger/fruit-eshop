from django.contrib import admin
from shop import models
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'price')
    search_fields = ('name',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('username', 'item', 'num')
    list_filter = ('username',)

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Cart, CartAdmin)
