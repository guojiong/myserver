from django.db import models


# Create your models here.

class Stock(models.Model):
    code = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    name = models.CharField(max_length=128, verbose_name='名称')
    origin = models.CharField(max_length=128, verbose_name='来源')
    remark = models.CharField(max_length=128, verbose_name='备注', null=True, blank=True)

    def __str__(self):
        return '[%s]' % self.name

    class Meta:
        ordering = ['-name']
        db_table = 'stock'
        verbose_name = '股票'
        verbose_name_plural = '股票'


class StockPrice(models.Model):
    code = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    name = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    startprice = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    yprice = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    nprice = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    hprice = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    lprice = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    bidingprice = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    auctionprice = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    tradingvolume = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    tradingprice = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy1 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy1price1 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy2 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy2price = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy3 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy3price = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy4 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy4price = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy5 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    buy5price = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale1 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale1price = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale2 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale2price = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale3 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale3price = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale4 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale4price = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale5 = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    sale5price = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32),
    date = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    date,
    time = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    time,
    status = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    varchar(32))
    def __str__(self):
        return

    class Meta:
        ordering = ['']
