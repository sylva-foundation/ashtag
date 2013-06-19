from model_utils.managers import QueryManager

from oscar.apps.catalogue.models import Product


class TagPackManager(QueryManager):
    def __init__(self, *args, **kwargs):
        super(TagPackManager, self).__init__(product_class__slug='tag-packs', *args, **kwargs)

    def order_by_tags(self, reverse=False):
        return sorted(self.all(), key=lambda p: p.num_tags, reverse=reverse)


class TagPack(Product):

    objects = TagPackManager()

    class Meta:
        proxy = True

    @property
    def num_tags(self):
        if not hasattr(self, '_num_tags'):
            self._num_tags = self.attribute_values.get(attribute__code='num_tags_in_pack').value
        return self._num_tags
