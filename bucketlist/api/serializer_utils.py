from rest_framework.reverse import reverse
from rest_framework.serializers import HyperlinkedIdentityField


class ParameterisedHyperlinkedIdentityField(HyperlinkedIdentityField):
    """
    Subclasses a HyperlinkedIdentityField to
    accept none or multiple lookup_fields.

    lookup_fields is a tuple of tuples of the form:
        ('model_field', 'url_parameter')

    Credits: This class definition/technique was
    originally suggested by millarm at:
    https://github.com/tomchristie/django-rest-framework/issues/1024
    """

    lookup_fields = (('pk', 'pk'),)

    def __init__(self, *args, **kwargs):
        self.lookup_fields = kwargs.pop('lookup_fields', self.lookup_fields)
        super(ParameterisedHyperlinkedIdentityField, self)\
            .__init__(*args, **kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.
        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        kwargs = {}
        for model_field, url_param in self.lookup_fields:
            attr = obj
            for field in model_field.split('.'):
                attr = getattr(attr, field)
            kwargs[url_param] = attr

        return reverse(view_name, kwargs=kwargs,
                       request=request, format=format)
