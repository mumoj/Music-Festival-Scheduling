from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from allauth.utils import build_absolute_uri

from django.http import HttpResponseRedirect
from django.urls import reverse


class UserAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        middle_name = data.get('middle_name')

        if middle_name:
            user_field(user, 'middle_name', middle_name)

        return super().save_user(request, user, form, commit=commit)

    def respond_email_verification_sent(self, request, user):
        return HttpResponseRedirect(reverse("accounts:account_email_verification_sent"))

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.

        Note that if you have architected your system such that email
        confirmations are sent outside of the request context `request`
        can be `None` here.
        """
        url = reverse("accounts:account_confirm_email", args=[emailconfirmation.key])
        ret = build_absolute_uri(request, url)
        return ret
