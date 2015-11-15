from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from utils import HTML5RequiredMixin

from models import BucketList, BucketListItem


class SignupForm(HTML5RequiredMixin, UserCreationForm):
    """ 
    Form that creates a user from the given username and password
    """
    password2 = forms.CharField(label="Confirm Password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.")



class SigninForm(HTML5RequiredMixin, AuthenticationForm):
    """ 
    Form for authenticating users with their username and password
    """
    def confirm_login_allowed(self, user):
        """ 
        overrides the default method to ensure that users can still 
        log in with is_active=False
        """
        pass



class BucketListForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    class Meta:
        model = BucketList
        fields = ('name', 'description',)

    def __init__(self, *args, **kwargs):
        super(BucketListForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True



class BucketListItemForm(HTML5RequiredMixin, forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    class Meta:
        model = BucketListItem
        fields = ('name', 'description', 'done')

