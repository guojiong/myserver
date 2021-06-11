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
    name = models.CharField(max_length=128, verbose_name='股票名称')
    startprice = models.CharField(max_length=128, verbose_name='今开')
    yprice = models.CharField(max_length=128, verbose_name='昨收')
    nprice = models.CharField(max_length=128, verbose_name='当前价格')
    hprice = models.CharField(max_length=128, verbose_name='最高价')
    lprice = models.CharField(max_length=128, verbose_name='最低价')
    bidingprice = models.CharField(max_length=128, verbose_name='竞买价')
    auctionprice = models.CharField(max_length=128, verbose_name='竞卖价')
    tradingvolume = models.CharField(max_length=128, verbose_name='成交量')
    tradingamount = models.CharField(max_length=128, verbose_name='成交金额')
    buy1 = models.CharField(max_length=128, verbose_name='买一量')
    buy1price1 = models.CharField(max_length=128, verbose_name='买一')
    buy2 = models.CharField(max_length=128, verbose_name='买二量')
    buy2price = models.CharField(max_length=128, verbose_name='买二')
    buy3 = models.CharField(max_length=128, verbose_name='买三量')
    buy3price = models.CharField(max_length=128, verbose_name='买三')
    buy4 = models.CharField(max_length=128, verbose_name='买四量')
    buy4price = models.CharField(max_length=128, verbose_name='买四')
    buy5 = models.CharField(max_length=128, verbose_name='买五量')
    buy5price = models.CharField(max_length=128, verbose_name='买五')
    sale1 = models.CharField(max_length=128, verbose_name='卖一量')
    sale1price = models.CharField(max_length=128, verbose_name='卖一')
    sale2 = models.CharField(max_length=128, verbose_name='卖二量')
    sale2price = models.CharField(max_length=128, verbose_name='卖二')
    sale3 = models.CharField(max_length=128, verbose_name='卖三量')
    sale3price = models.CharField(max_length=128, verbose_name='卖三')
    sale4 = models.CharField(max_length=128, verbose_name='卖四量')
    sale4price = models.CharField(max_length=128, verbose_name='卖四')
    sale5 = models.CharField(max_length=128, verbose_name='卖五量')
    sale5price = models.CharField(max_length=128, verbose_name='卖五')
    date = models.DateField(max_length=128, unique=True, verbose_name='日期')
    time = models.TimeField(max_length=128, unique=True, verbose_name='时间')
    status = models.CharField(max_length=128, verbose_name='状态')

    def __str__(self):
        return '[%s]' % self.name

    class Meta:
        ordering = ['time']
        db_table = 'stockprice'
        verbose_name = '分时量价'
        verbose_name_plural = '分时量价'


class CollectorStatus(models.Model):
    ident = models.CharField(max_length=128, unique=True, verbose_name='线程id')
    status = models.IntegerField(unique=True, verbose_name='状态')

    def __str__(self):
        return '[%s]' % self.status

    class Meta:
        db_table = 'CollectorStatus'
        verbose_name = '采集器状态'
        verbose_name_plural = '采集器状态'


class LbHsl(models.Model):
    code = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    date = models.DateField(verbose_name='日期')
    startprice = models.CharField(max_length=128, verbose_name='开盘价')
    hprice = models.CharField(max_length=128, verbose_name='最高价')
    eprice = models.CharField(max_length=128, verbose_name='收盘价')
    lprice = models.CharField(max_length=128, verbose_name='最低价')
    volume = models.CharField(max_length=128, verbose_name='成交量')
    rfprice = models.CharField(max_length=128, verbose_name='涨跌额')
    applies = models.CharField(max_length=128, verbose_name='涨跌幅')
    daily5price = models.CharField(max_length=128, verbose_name='5日均价')
    daily10price = models.CharField(max_length=128, verbose_name='10日均价')
    daily20price = models.CharField(max_length=128, verbose_name='20日均价')
    daily5volume = models.CharField(max_length=128, verbose_name='5日均量')
    daily10volume = models.CharField(max_length=128, verbose_name='10日均量')
    daily20volume = models.CharField(max_length=128, verbose_name='20日均量')
    turnoverrate = models.CharField(max_length=128, verbose_name='换手率')

    def __str__(self):
        return '[%s]' % self.code

    class Meta:
        ordering = ['date']
        db_table = 'lbhsl'
        verbose_name = '量比换手率'
        verbose_name_plural = '量比换手率'


class LbHsl2(models.Model):
    code = models.CharField(max_length=128, unique=True, verbose_name='股票代码')
    date = models.DateField(verbose_name='日期')
    volume = models.CharField(max_length=128, verbose_name='成交量')
    turnoverrate = models.CharField(max_length=128, verbose_name='换手率')
    time = models.TimeField(verbose_name='时间')
    circulation = models.IntegerField(verbose_name='流通量')

    def __str__(self):
        return '[%s]' % self.code

    class Meta:
        db_table = 'lbhsl2'
        verbose_name = '量比换手率'
        verbose_name_plural = '量比换手率'


class hq_history(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name='股票代码')
    date = models.DateField(verbose_name='日期')
    sprice = models.FloatField(max_length=10, verbose_name='开盘价')
    hprice = models.FloatField(max_length=10, verbose_name='最高价')
    eprice = models.FloatField(max_length=10, verbose_name='收盘价')
    lprice = models.FloatField(max_length=10, verbose_name='最低价')
    volume = models.IntegerField(verbose_name='成交量')
    changeamount = models.FloatField(max_length=20, verbose_name='涨跌额')
    changerange = models.FloatField(max_length=10, verbose_name='涨跌幅')
    p5 = models.FloatField(max_length=10, verbose_name='5日均价')
    p10 = models.FloatField(max_length=10, verbose_name='10日均价')
    p20 = models.FloatField(max_length=10, verbose_name='20日均价')
    v5 = models.IntegerField(verbose_name='5日均量')
    v10 = models.IntegerField(verbose_name='10日均量')
    v20 = models.IntegerField(verbose_name='20日均量')
    hsl = models.FloatField(max_length=10, verbose_name='换手率')
