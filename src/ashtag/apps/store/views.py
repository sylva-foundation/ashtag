from django.views.generic import TemplateView

from oscar.apps.catalogue.models import Product


class TagPacksView(TemplateView):
    template_name = 'store/tag-packs.html'

    def get_context_data(self, **kwargs):
        context = super(TagPacksView, self).get_context_data(**kwargs)

        products = Product.objects.filter(product_class__slug="tag-pack")
        products = filter(lambda p: p.is_available_to_buy, products)
        context['products'] = products

        return context
