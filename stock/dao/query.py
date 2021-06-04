from django.core import serializers

from stock.models import Stock


def query(code=None, name=None, origin=None, remark=None):
    search_condition = {}
    if code:
        search_condition['code__contains'] = code
    if name:
        search_condition['name__contains'] = name
    if origin:
        search_condition['origin__contains'] = origin
    stocks = serializers.serialize('json', Stock.objects.filter(**search_condition))
    return stocks