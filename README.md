# 简易水果电商

基于py3 + Django2.0的简单购物系统.

## 登录注册

使用Django提供的Auth模块进行注册登录登出功能.


## 主页

使用Bootstrap搭建前端页面, 使用Django提供的paginator进行分页.

![主页](https://github.com/EwdAger/fruit-eshop/blob/master/screenshot/1.png)

## 后台

使用Django提供的Admin模块进行新商品的添加删除.

## 购物车

比较愚蠢的将购物车信息写进了数据库..

```python
class Cart(models.Model):
    username = models.CharField(max_length=20, verbose_name="用户名")
    item = models.CharField(max_length=200, verbose_name="产品名称")
    num = models.DecimalField(max_digits=2, decimal_places=0, default=0, verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="价格")
```

所以每次进行商品的添加删除增减数量都必须连接一次数据库....

## Update

**2018-5-9 添加**
- 添加订单系统
- 添加库存显示与相关逻辑