from django.core import serializers

from stock.models import Stock, CollectorStatus


def q_stock(code=None, name=None, origin=None, remark=None):
    search_condition = {}
    if code:
        search_condition['code__contains'] = code
    if name:
        search_condition['name__contains'] = name
    if origin:
        search_condition['origin__contains'] = origin
    if remark:
        search_condition['remark__contains'] = remark
    stocks = serializers.serialize('json', Stock.objects.filter(**search_condition))
    return stocks


def q_collectorstatus():
    collectorstatus = serializers.serialize('json', CollectorStatus.objects.filter(status=1))
    return collectorstatus