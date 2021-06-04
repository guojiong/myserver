from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class StockConfig(AppConfig):
    name = 'stock'

    def ready(self):
        autodiscover_modules('tests.py')
