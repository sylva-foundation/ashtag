from django.conf import settings


def enable_tracking(request):
    return {
        'ENABLE_TRACKING_CODE': settings.ENABLE_TRACKING_CODE,
    }


def image_sizes(request):
    context = {}
    for k, v in settings.IMAGE_SIZES.items():
        context["IMG_%s" % k.upper()] = v
    return context
