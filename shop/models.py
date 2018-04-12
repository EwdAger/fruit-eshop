# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    sku = models.CharField(max_length=20, verbose_name="产品编号")
    name = models.CharField(max_length=200, verbose_name="产品名称")
    description = models.TextField(verbose_name="描述")
    image = models.URLField(null=True, verbose_name="图片地址")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="价格")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "产品目录"
        verbose_name_plural = "产品目录"


class Cart(models.Model):
    username = models.CharField(max_length=20, verbose_name="用户名")
    item = models.CharField(max_length=200, verbose_name="产品名称")
    num = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name="数量")

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = "用户购物车"
        verbose_name_plural = "用户购物车"