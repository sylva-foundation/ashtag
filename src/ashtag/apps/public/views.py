import json

from django.http import HttpResponse
from django.views.generic import View


class AuthStatusView(View):
    def get(self, request, *args, **kwargs):
        out = json.dumps({"authenticated": request.user.is_authenticated()})
        return HttpResponse(out, content_type="application/json")
