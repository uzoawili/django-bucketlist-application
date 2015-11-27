from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.conf import settings
from django.views.generic.edit import UpdateView
from django.views.generic import View, ListView,\
    DetailView, CreateView, DeleteView

from models import BucketList, BucketListItem
from forms import SignupForm, SigninForm,\
    BucketListForm, BucketListItemForm


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class IndexView(View):

    """
    Represents the landing/Home/authentication view.
    """

    validation_msgs = {
        'invalid_params': 'Invalid username or password!',
        'auth_error': 'Oops, an error occured! Try again.',
    }

    def get(self, request, *args, **kwargs):
        """
        Renders the index/home view
        """

        # redirect to dashboard/bucketlists if user is already signed in:
        if request.user.is_authenticated():
            return redirect(reverse('dashboard:bucketlists'))

        # otherwise show home view:
        return self.render_home_view()

    def post(self, request, *args, **kwargs):
        """
        Handles the signin and signup form submissions
        """
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

        else:
            return self.render_home_view()

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

            else:
                messages.error(request, self.validation_msgs.get('auth_error'))
        else:
            messages.error(request, self.validation_msgs.get('invalid_params'))

        # render with invalid form and msgs:
        return self.render_home_view(**{
            auth_form_name: auth_form,
            'active_auth_index': active_auth_index,
        })

    def render_home_view(self,
                         signup_form=SignupForm(auto_id=True),
                         signin_form=SigninForm(auto_id=True),
                         active_auth_index=0
                         ):

        # otherwise show home view:
        context = {
            'signup_form': signup_form,
            'signin_form': signin_form,
            'active_auth_index': active_auth_index,
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


class BucketListsView(LoginRequiredMixin, ListView):

    """
    Returns a list of bucketlists created by this logged in user.
    """
    template_name = 'dashboard/bucketlists.html'
    ordering = ['-date_created', ]
    context_object_name = 'bucketlists'
    paginate_by = settings.DASHBOARD_PAGE_LIMIT

    def get_queryset(self):
        """
        Returns the queryset of bucketlists created by the current user.
        """
        # get any search param from the request:
        get_params = self.request.GET.dict()
        # get user's bucketlists:
        results = BucketList.objects.filter(created_by=self.request.user)
        # search if param is specified:
        self.search_query = get_params.get('q')
        if self.search_query:
            results = results.filter(name__icontains=self.search_query)

        return results

    def get_context_data(self, **kwargs):
        """
        Returns the context that will be used to render the template.
        """
        context = super(BucketListsView, self).get_context_data(**kwargs)
        context.update({
            'sidebar_tab_index': 1,
            'search_query': self.search_query or None,
            'title': 'My Bucket Lists',
        })
        return context


class BucketListEditView(LoginRequiredMixin):

    """
    Base class for BucketList create and update views.
    """
    form_class = BucketListForm
    template_name = 'dashboard/bucketlist_edit.html'
    success_toast = ''

    def get_success_url(self):
        """
        Determines the url to redirect to after processing a valid form
        """
        if self.success_toast:
            messages.info(self.request, self.success_toast)
        return reverse('dashboard:bucketlists')

    def get_queryset(self):
        """
        Determines the queryset to be used to get the current object
        """
        return BucketList.objects.filter(created_by=self.request.user)


class BucketListCreateView(BucketListEditView, CreateView):

    """
    View for creating a BucketList.
    """
    success_toast = 'Bucket List created, nice!'

    def get_context_data(self, **kwargs):
        """
        Returns the context that will used to render the view.
        """
        context = super(BucketListCreateView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Create Bucket List',
            'sidebar_tab_index': 1,
        })
        return context

    def form_valid(self, form):
        """
        Saves the object referenced by the form, 
        sets the current object for the view,
        and redirects to get_success_url()
        """
        bucketlist = form.save(commit=False)
        bucketlist.created_by = self.request.user
        bucketlist.save()
        self.object = bucketlist
        return redirect(self.get_success_url())


class BucketListUpdateView(BucketListEditView, UpdateView):

    """
    View for updating a BucketList.
    """
    success_toast = 'Bucket List updated, cool!'

    def get_context_data(self, **kwargs):
        """
        Returns the context that will used to render the view.
        """
        context = super(BucketListUpdateView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Update Bucket List',
            'sidebar_tab_index': 1,
        })
        return context


class BucketListDeleteView(BucketListEditView, DeleteView):

    """
    View for deleteing a BucketList.
    """
    success_toast = 'Bucket List discarded!'
    template_name = 'dashboard/bucketlist_delete.html'

    def get_context_data(self, **kwargs):
        """
        Returns the context that will used to render the view.
        """
        context = super(BucketListDeleteView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Update Bucket List',
            'sidebar_tab_index': 1,
        })
        return context


class BucketListDetailView(LoginRequiredMixin, DetailView):

    template_name = 'dashboard/bucketlist_details.html'
    context_object_name = 'bucketlist'

    def get_queryset(self):
        """ 
        Returns the queryset of bucketlists 
        created by the current user. 
        """
        # return user's bucketlists:
        return BucketList.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Returns the context that will used to render the template.
        """
        context = super(BucketListDetailView, self).get_context_data(**kwargs)
        context.update({
            'sidebar_tab_index': 1,
            'items': BucketListItem.objects.filter(bucketlist=self.object),
        })
        return context


class BucketListItemEditView(LoginRequiredMixin):

    """
    Base class for BucketListItem create and update views.
    """
    form_class = BucketListItemForm
    template_name = 'dashboard/bucketlist_item_edit.html'
    pk_url_kwarg = 'item_pk'
    success_toast = ''

    def get_success_url(self):
        """
        Determines the url to redirect to after processing a valid form
        """
        if self.success_toast:
            messages.info(self.request, self.success_toast)
        return reverse(
            'dashboard:bucketlist_details',
            kwargs={'pk': self.object.bucketlist.pk}
        )

    def get_queryset(self):
        """
        Determines the queryset to be used to get the list
        """
        bucketlist = self.get_current_bucketlist()
        return BucketListItem.objects.filter(bucketlist=bucketlist)

    def get_current_bucketlist(self):
        """
        Returns the bucketlist refrenced in the url:
        """
        return get_object_or_404(
            BucketList,
            created_by=self.request.user,
            pk=self.kwargs.get('pk')
        )


class BucketListItemCreateView(BucketListItemEditView, CreateView):

    """
    View for creating a BucketListItem.
    """
    success_toast = 'Item added to bucket list!'

    def get_context_data(self, **kwargs):
        """
        Returns the context that will used to render the view.
        """
        context = super(
            BucketListItemCreateView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Add New Item',
            'bucketlist': self.get_current_bucketlist(),
            'sidebar_tab_index': 1,
        })
        return context

    def form_valid(self, form):
        """
        Saves the object referenced by the form, 
        sets the current object for the view,
        and redirects to get_success_url()
        """
        item = form.save(commit=False)
        bucketlist = BucketList.objects.filter(
            created_by=self.request.user,
            pk=self.kwargs.get('pk')
        )
        item.bucketlist = self.get_current_bucketlist()
        item.save()
        self.object = item
        return redirect(self.get_success_url())


class BucketListItemUpdateView(BucketListItemEditView, UpdateView):

    """
    View for updating a BucketListItem.
    """
    success_toast = 'Item updated, cool!'

    def get_context_data(self, **kwargs):
        """
        Returns the context that will be used to render the view.
        """
        context = super(
            BucketListItemUpdateView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Update Item',
            'bucketlist': self.get_current_bucketlist(),
            'sidebar_tab_index': 1,
        })
        return context


class BucketListItemDoneView(BucketListItemEditView, View):

    """
    View for updating the 'done' property of a BucketListItem.
    """
    success_toast = 'Item marked as done, keep it up!'

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to this view.
        """

        if 'done' in request.POST:
            item = self.get_queryset().filter(pk=kwargs.get('item_pk')).get()
            item.done = True
            item.save()
            self.object = item
            return redirect(self.get_success_url())
        else:
            raise Http404()


class BucketListItemDeleteView(BucketListItemEditView, DeleteView):

    """
    View for deleteing a BucketListItem.
    """
    success_toast = 'Item discarded!'
    template_name = 'dashboard/bucketlist_item_delete.html'

    def get_context_data(self, **kwargs):
        """
        Returns the context that will used to render the view.
        """
        context = super(
            BucketListItemDeleteView, self).get_context_data(**kwargs)
        context.update({
            'title': 'Delete Bucket List',
            'bucketlist': self.get_current_bucketlist(),
            'sidebar_tab_index': 1,
        })
        return context
