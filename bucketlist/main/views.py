from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.context_processors import csrf
from django.core.validators import ValidationError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView

from django.http import HttpResponse

from models import BucketList
from forms import SignupForm, SigninForm


class IndexView(View):

    validation_msgs = {
        'invalid_params': 'Invalid username or password!',
        'user_already_exists': 'Sorry, that username is taken.',
        'auth_error': 'Oops, an error occured! Try again.'
    }

    def get(self, request, *args, **kwargs):
        
        # redirect to dashboard/bucketlists if user is already signed in:
        if request.user.is_authenticated():
            return redirect(reverse('dashboard:bucketlists'))
        
        # otherwise show home view:
        return self.render_home_view()


    def post(self, request, *args, **kwargs):
        
        if 'signup' in request.POST:

            signup_form = SignupForm(request.POST, auto_id=True)
            validation_msg = ""

            if signup_form.is_valid():
                # get the auth params:
                username = signup_form['username'].value()
                password = signup_form['password1'].value()
                # ensure it's not an existing user:
                try:
                    user = User.objects.get(username=username)
                    validation_msg = self.validation_msgs.get('user_already_exists')
                except ObjectDoesNotExist:
                    # save the new user to db:
                    signup_form.save()
                    # authenticate & log the created user in:
                    if self.authenticate_and_login(username, password):
                        # redirect to the dashboard/bucketlists view:
                        return redirect(reverse('dashboard:bucketlists'))
                    else: 
                        validation_msg = self.validation_msgs.get('auth_error')
            else: 
                validation_msg = self.validation_msgs.get('invalid_params')
            
            # render with invalid form and msgs:
            return self.render_home_view(signup_form=signup_form, validation_msg=validation_msg)

        
        elif 'signin' in request.POST:

            signin_form = SigninForm(request.POST, auto_id=True)
            validation_msg = ""
            
            if signin_form.is_valid():
                # get the auth params:
                username = signup_form['username'].value()
                password = signup_form['password'].value()
                # authenticate & log the created user in:
                if self.authenticate_and_login(username, password):
                    # redirect to the dashboard:
                    return redirect(reverse('dashboard:bucketlists'))
                else: 
                    validation_msg = self.validation_msgs.get('auth_error')
            else: 
                validation_msg = self.validation_msgs.get('invalid_params')
        
        else: 
            return self.render_home_view()


    def render_home_view( self,
        signup_form = SignupForm(auto_id=True), 
        signin_form = SigninForm(auto_id=True), 
        active_auth_index = 0,
        validation_msg = ""
    ):
        # otherwise show home view:
        context = {
            'signup_form': signup_form,
            'signin_form': signin_form,
            'active_auth_index': active_auth_index,
            'validation_msg': validation_msg,
        }
        context.update(csrf(self.request))
        return render(self.request, 'main/home.html', context)


    def authenticate_and_login(self, username, password):
        try:
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return user
        except:
            return None


# class BucketListsView(ListView):
class BucketListsView(View):
    # context_object_name = 'bucketlists'
    # queryset = BucketList.objects.filter(publisher__name='Acme Publishing')
    # template_name = 'main/bucketlists.html'

    def get(self, request, *args, **kwargs):
        
        # otherwise show home view:
        return HttpResponse("Signed in!")

    def post(self, request, *args, **kwargs):
        
        # otherwise show home view:
        return HttpResponse("Signed in!")

