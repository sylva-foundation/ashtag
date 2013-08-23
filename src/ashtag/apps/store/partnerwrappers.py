from decimal import Decimal as D

from django.conf import settings

from oscar.apps.partner.wrappers import DefaultWrapper


class AdaptWrapper(DefaultWrapper):

    def calculate_tax(self, stockrecord):
        tax = stockrecord.price_excl_tax * D(settings.OSCAR_TAX)
        return tax.quantize(D('0.01'))
