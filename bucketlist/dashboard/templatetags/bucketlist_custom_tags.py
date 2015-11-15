from django import template

# instantiate a template library:
register = template.Library()


@register.filter(name='widget_name')
def fieldtype(field):
    """ Returns the widget element name of a django form field as a string """
    return field.field.widget.__class__.__name__