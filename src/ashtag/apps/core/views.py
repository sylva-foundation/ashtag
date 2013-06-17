from django.conf import settings

from registration.backends.simple.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail


class AshTagRegistrationView(RegistrationView):
    form_class = RegistrationFormUniqueEmail

    def get_success_url(self, request, user):
        return (settings.LOGIN_REDIRECT_URL, (), {})
