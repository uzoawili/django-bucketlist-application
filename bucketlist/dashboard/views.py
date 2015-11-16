from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.validators import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView
from django.conf import settings

from models import BucketList
from forms import SignupForm, SigninForm, BucketListForm, BucketListItemForm
from utils import SerializedHtmlResponse



class IndexView(View):

    validation_msgs = {
        'invalid_params': 'Invalid username or password!',
        'auth_error': 'Oops, an error occured! Try again.',
    }

    def get(self, request, *args, **kwargs):
        
        # redirect to dashboard/bucketlists if user is already signed in:
        if request.user.is_authenticated():
            return redirect(reverse('dashboard:bucketlists'))
        
        # otherwise show home view:
        return self.render_home_view()


    def post(self, request, *args, **kwargs):
        if 'signup' in request.POST:
            auth_form_name = 'signup_form'
            auth_form = SignupForm(request.POST, auto_id=True)
            password_field_name = 'password1'
            active_auth_index = 0
        
        elif 'signin' in request.POST:
            auth_form_name = 'signin_form'
            auth_form = SigninForm(data=request.POST, auto_id=True)
            password_field_name = 'password'
            active_auth_index = 1

        else:  return self.render_home_view()

        if auth_form.is_valid():
            # get the auth params:
            username = auth_form['username'].value()
            password = auth_form[password_field_name].value()
            # when signing up, save the new user to db:
            if auth_form_name == 'signup_form':
                auth_form.save()
            # authenticate & log the user in:
            if self.authenticate_and_login(username, password):
                # redirect to the dashboard/bucketlists view:
                return redirect(reverse('dashboard:bucketlists'))
            
            else: messages.error(request, self.validation_msgs.get('auth_error'))
        else: messages.error(request, self.validation_msgs.get('invalid_params'))
        
        # render with invalid form and msgs:
        return self.render_home_view(**{
            auth_form_name: auth_form,
            'active_auth_index': active_auth_index,
        }) 


    def render_home_view(self, \
        signup_form = SignupForm(auto_id=True), \
        signin_form = SigninForm(auto_id=True), \
        active_auth_index = 0000, \
        validation_msg = "" \
        ):

        # otherwise show home view:
        context = {
            'signup_form': signup_form,
            'signin_form': signin_form,
            'active_auth_index': active_auth_index,
            'validation_msg': validation_msg,
        }
        context.update(csrf(self.request))
        return render(self.request, 'dashboard/home.html', context)


    def authenticate_and_login(self, username, password):
        try:
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return user
        except:
            return None



class BucketListsView(View):
    

    validation_msgs = {
        'invalid_params': 'Some required fields were omitted or invalid',
    }


    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BucketListsView, self).dispatch(*args, **kwargs)


    def get(self, request, *args, **kwargs):
        """ 
        Shows all [or searches] the bucketlists created by the current user. 
        """
        # get any search options from the request:
        options = request.GET.dict()
        # get user's bucketlists:
        results = BucketList.objects.filter(creator=request.user)
        # search if query is specified:
        q = options.get('q')
        if q:
            results = BucketList.objects.filter(name__icontains=q)
        # prepare the context:
        context = {
            'bucketlists': results.all(),
            'sidebar_tab_index': 1,
            'bucketlist_form': BucketListForm(auto_id=True),
        }
        context.update(csrf(request))
        # return the rendered template response:
        return render(request, 'dashboard/bucketlists.html', context)


    def post(self, request, *args, **kwargs):
        """ 
        Creates a new bucket list for the current user. 
        """
        bucketlist_form = BucketListForm(request.POST, auto_id=True)

        if bucketlist_form.is_valid():
            # save the bucket list to db:
            bucketlist = bucketlist_form.save(commit=False)
            bucketlist.creator = request.user
            bucketlist.save()
            # render and return the created bucketlist's thumbnail:
            return SerializedHtmlResponse (
                request, 
                context_dict = {'bucketlist': bucketlist}, 
                template_name = 'dashboard/snippet_bucketlist_thumb.html', 
                operation = SerializedHtmlResponse.CREATE_BUCKET_LIST, 
                status = SerializedHtmlResponse.SUCCESS
            )

        else: messages.error(request, self.validation_msgs.get('invalid_params'))

        # return the rendered modal with invalid form:
        return SerializedHtmlResponse (
            request, 
            context_dict = {'form': bucketlist_form}, 
            template_name = 'dashboard/snippet_bucketlist_form.html', 
            operation = SerializedHtmlResponse.CREATE_BUCKET_LIST, 
            status = SerializedHtmlResponse.INVALID
        )
 






