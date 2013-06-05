import os

from django.http import HttpResponse


def show_env(request):
	return HttpResponse(repr(os.environ))
	# return HttpResponse("Disabled")