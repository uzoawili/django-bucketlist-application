from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.core.validators import ValidationError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import View


from forms import SignupForm, SigninForm


class HomeView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'signup_form': SignupForm(auto_id=True),
            'signin_form': SigninForm(auto_id=True),
        }
        context.update(csrf(request))
        return render(request, 'main/index.html', context)

    # def post(self, request, *args, **kwargs):
    #     email_form = EmailForm(request.POST, auto_id=True)
    #     if email_form.is_valid():
    #         try:
    #             # get the account for that email if it exists:
    #             input_email = email_form.cleaned_data.get('email')
    #             registered_user = User.objects.get(email__exact=input_email)

    #             # generate a recovery hash url for that account:
    #             recovery_hash = Hasher.gen_hash(registered_user)
    #             recovery_hash_url = request.build_absolute_uri(
    #                 reverse(
    #                     'account_reset_password',
    #                     kwargs={'recovery_hash': recovery_hash}
    #                 ))

    #             # compose the email:
    #             recovery_email_context = RequestContext(
    #                 request,
    #                 {'recovery_hash_url': recovery_hash_url})
    #             recovery_email = Mailgunner.compose(
    #                 sender='Troupon <troupon@andela.com>',
    #                 recipient=registered_user.email,
    #                 subject='Troupon: Password Recovery',
    #                 html=loader.get_template(
    #                     'account/forgot_password_recovery_email.html'
    #                     ).render(recovery_email_context),
    #                 text=loader.get_template(
    #                     'account/forgot_password_recovery_email.txt'
    #                     ).render(recovery_email_context),
    #             )
    #             # send it and get the request status:
    #             email_status = Mailgunner.send(recovery_email)

    #             # inform the user of the status of the recovery mail:
    #             context = {
    #                 'page_title': 'Forgot Password',
    #                 'registered_user':  registered_user,
    #                 'recovery_mail_status': email_status,
    #             }
    #             return render(
    #                 request,
    #                 'account/forgot_password_recovery_status.html',
    #                 context)

    #         except ObjectDoesNotExist:
    #             # set an error message:
    #             messages.add_message(
    #                 request, messages.ERROR,
    #                 'The email you entered does not \
    #                 belong to a registered user!')

    #     context = {
    #         'page_title': 'Forgot Password',
    #         'email_form': email_form,
    #     }
    #     context.update(csrf(request))
    #     return render(request, 'account/forgot_password.html', context)
