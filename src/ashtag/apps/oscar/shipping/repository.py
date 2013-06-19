from oscar.apps.shipping.repository import Repository as BaseRepository
from oscar.apps.shipping.models import OrderAndItemCharges


class Repository(BaseRepository):

    def get_shipping_methods(self, user, basket, shipping_addr=None, *args, **kwargs):
        methods = []
        for m in OrderAndItemCharges.objects.all():
            m.set_basket(basket)
            methods.append(m)
        return methods
