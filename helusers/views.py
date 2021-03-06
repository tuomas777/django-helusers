from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.views.generic.base import RedirectView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class LogoutView(DjangoLogoutView):
    def dispatch(self, request, *args, **kwargs):
        was_authenticated = request.user.is_authenticated
        session = request.session
        end_session_url = session.get('social_auth_end_session_url')
        if end_session_url:
            self.next_page = end_session_url
        ret = super().dispatch(request, *args, **kwargs)
        if was_authenticated:
            messages.success(request, _("You have been successfully logged out."))
        return ret


class LogoutCompleteView(DjangoLogoutView):
    def dispatch(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_next_page())


class LoginView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        url = reverse('social:begin', kwargs=dict(backend='tunnistamo'))
        redirect_to = self.request.GET.get(REDIRECT_FIELD_NAME)
        if redirect_to:
            url += '?%s=%s' % (REDIRECT_FIELD_NAME, redirect_to)
        return url
