import json

from django.http import HttpResponse
from django.views.generic import View, RedirectView


class AuthStatusView(View):
    def get(self, request, *args, **kwargs):
        out = json.dumps({
            "authenticated": request.user.is_authenticated(),
            "phonegap": bool(request.session.get('phonegap', False)),
        })
        return HttpResponse(out, content_type="application/json")


class PhoneGapView(RedirectView):
    url = '/'

    def get_redirect_url(self, **kwargs):
        if self.request.GET.get('disable') and self.request.session.get('phonegap', False):
            del self.request.session['phonegap']
        else:
            self.request.session['phonegap'] = True
        return super(PhoneGapView, self).get_redirect_url(**kwargs)
