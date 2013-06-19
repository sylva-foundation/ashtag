from django.views.generic import TemplateView

from ashtag.apps.store.models import TagPack


class TagPacksView(TemplateView):
    template_name = 'store/tag-packs.html'

    def get_context_data(self, **kwargs):
        context = super(TagPacksView, self).get_context_data(**kwargs)

        products = TagPack.objects.order_by_tags()
        products = filter(lambda p: p.is_available_to_buy, products)
        context['products'] = products

        return context
