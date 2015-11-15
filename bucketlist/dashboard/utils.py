import json

from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import HiddenInput, FileInput
from django.template import loader, RequestContext
from django.http import HttpResponse



class HTML5RequiredMixin(object):
    """
    Adds HTML5 'required' attribute and behaviour to django form fields.
    Asteriks '*' are also added to the field labels as a visual cue.
    """

    def __init__(self, *args, **kwargs):
        # initialize with super class constructor:
        super(HTML5RequiredMixin, self).__init__(*args, **kwargs)
        # iterate over the fields in the form:
        for field in self.fields:
            # select only required fields that are niether prefixed 
            # nor AdminFileWidget, HiddenInput, FileInput
            if (
                self.fields[field].required and
                type(self.fields[field].widget) not in (AdminFileWidget, HiddenInput, FileInput) and 
                '__prefix__' not in self.fields[field].widget.attrs
            ):
                # add the HTNL5 'required' atrribute to the widget:
                self.fields[field].widget.attrs['required'] = 'required'
                # add asteriks to the label as a visual cue:
                if self.fields[field].label:
                    self.fields[field].label += ' *'


class SerializedHtmlResponse(HttpResponse):
    """
    Represents a HttpResponse whose JSON formatted contents contains
    the operation, status_text and html response to an AJAX request
    from the bucketlist app client.
    """

    # operations:
    CREATE_BUCKET_LIST = 'create_bucket_list'
    UPDATE_BUCKET_LIST = 'update_bucket_list'
    DELETE_BUCKET_LIST = 'delete_bucket_list'
    CREATE_BUCKET_LIST_ITEM = 'create_bucket_list_item'
    UPDATE_BUCKET_LIST_ITEM = 'update_bucket_list_item'
    DELETE_BUCKET_LIST_ITEM = 'delete_bucket_list_item'

    # status texts:
    SUCCESS = 'success'
    INVALID = 'invalid'


    def __init__(self, request, context_dict, template_name, operation, status_text):
        # prepare the request context:
        context = RequestContext(request, context_dict)
        # get the template:
        template = loader.get_template(template_name)
        # render the template to a string: 
        rendered_template = template.render(context)
        # prepare the json response data:
        json_response = json.dumps({
            'operation': operation,
            'status_text': status_text,
            'html': rendered_template,
        })
        # set the response status code
        status_code = 200
        if(operation == self.CREATE_BUCKET_LIST or \
           operation == self.CREATE_BUCKET_LIST_ITEM) and \
           status_text == self.SUCCESS:
            status_code = 201

        # initialize the HttpResponse with this content:
        super(SerializedHtmlResponse, self).__init__(
            content=json_response, 
            status=status_code
        )





