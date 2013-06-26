from decimal import Decimal as D

from django.conf import settings

from oscar.apps.partner.wrappers import DefaultWrapper


class AdaptWrapper(DefaultWrapper):

    def calculate_tax(self, stockrecord):
        return stockrecord.price_excl_tax * D(settings.OSCAR_TAX)
