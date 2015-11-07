from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from models import BucketList, BucketListItem


class SignupForm(UserCreationForm):
    """
    Form that creates a user from the given username and password
    """
    class Meta:
        model = User
        fields = ('username','password1', 'password2')


class SigninForm(AuthenticationForm):
    """
    Form for authenticating users with their username and password
    """
    def confirm_login_allowed(self, user):
        """
        overrides the default method to ensure that
        users can still log in with is_active=False
        """
        pass


