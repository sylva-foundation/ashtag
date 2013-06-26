from django.conf import settings


def enable_tracking(request):
    return {
        'ENABLE_TRACKING_CODE': settings.ENABLE_TRACKING_CODE,
    }
