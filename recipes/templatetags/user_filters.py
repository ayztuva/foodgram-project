from django import template

from recipes.models import Purchase

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})

