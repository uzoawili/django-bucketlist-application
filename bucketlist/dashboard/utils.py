from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import HiddenInput, FileInput


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
                type(self.fields[field].widget) not in
                (AdminFileWidget, HiddenInput, FileInput) and
                '__prefix__' not in self.fields[field].widget.attrs
            ):
                # add the HTNL5 'required' atrribute to the widget:
                self.fields[field].widget.attrs['required'] = 'required'
                # add asteriks to the label as a visual cue:
                if self.fields[field].label:
                    self.fields[field].label += ' *'
