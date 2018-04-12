# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="产品分类")

    class Meta:
        verbose_name = "产品类型"
        verbose_name_plural = "产品类型"
    def __unicode__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="产品分类")
    sku = models.CharField(max_length=20, verbose_name="产品编号")
    name = models.CharField(max_length=200, verbose_name="产品名称")
    description = models.TextField(verbose_name="描述")
    image = models.URLField(null=True, verbose_name="图片地址")
    website = models.URLField(null=True, verbose_name="产品网址")
    stock = models.PositiveIntegerField(default=0, verbose_name="库存数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="价格")

    class Meta:
        verbose_name = "产品目录"
        verbose_name_plural = "产品目录"
    def __unicode__(self):
        return self.name

