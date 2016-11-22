from django import template

register = template.Library()


@register.filter
def format_euro(euro_db):
    return "{0:.2f}".format(float(euro_db)/100).replace('.', ',')
