from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def to_list(value):
    items = value.split(',')
    items = map(lambda s: s.strip(), items)
    items = filter(bool, items)
    return items