from django import template

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css_class):

    """ Renders a bound form field with an extra CSS class merged
    into its widget's existing attrs, so Bootstrap's form-control
    styling can be applied to any field from inside a template
    without a whole extra package for one filter. """

    return field.as_widget(attrs={"class": css_class})