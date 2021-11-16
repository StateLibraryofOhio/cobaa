from django import template

from cobaa.settings.base import STATIC_ROOT

register = template.Library()


# See: https://github.com/xhtml2pdf/xhtml2pdf/issues/388

@register.filter
def to_absolute(img):
    return str(STATIC_ROOT) + img
