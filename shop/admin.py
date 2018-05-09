from django.contrib import admin
from shop import models
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'sku')
    search_fields = ('name',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('username', 'item', 'num', 'price')
    list_filter = ('username',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'username', 'date')
    list_filter = ('date',)
    search_fields = ('name',)

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Cart, CartAdmin)
admin.site.register(models.Order, OrderAdmin)
