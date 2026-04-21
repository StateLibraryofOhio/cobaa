from pathlib import Path

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders

register = template.Library()


# See: https://github.com/xhtml2pdf/xhtml2pdf/issues/388

@register.filter
def to_absolute(asset_path):
    normalized_path = str(asset_path).lstrip("/")
    located = finders.find(normalized_path)
    if isinstance(located, (list, tuple)):
        located = located[0] if located else None
    if located:
        return located
    return str(Path(settings.STATIC_ROOT) / normalized_path)
